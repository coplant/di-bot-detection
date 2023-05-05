import asyncio
from hashlib import sha1

from celery import Celery
from fuzzywuzzy import fuzz
from sqlalchemy import select

from proxy.src.assessment import utils
from proxy.src.database import async_session_maker
from proxy.src.config import REDIS_URL, FP_PRIORITY, LS_RATIO_MIN, LS_RATIO_MAX, FP_RATIO
from proxy.src.service.schemas import FingerprintSchema
from proxy.src.service.models import User, Cookie

celery = Celery("analyzing", broker=REDIS_URL, backend=REDIS_URL)


async def get_similar_hashes(user_long_hash):
    async with async_session_maker() as session:
        query = select(User.hash)
        result = await session.execute(query)
        db_hashes = result.scalars().all()
        matches = []
        match = None
        for hash_from_db in db_hashes:
            ratio = fuzz.WRatio(hash_from_db, user_long_hash)
            if ratio > LS_RATIO_MIN:
                matches.append((hash_from_db, ratio))
        if matches:
            match = max(matches, key=lambda x: x[1])
        return match


async def get_current_user(long_hash: str):
    match = await get_similar_hashes(long_hash)
    async with async_session_maker() as session:
        if not match:
            return None
        query = select(User).filter_by(hash=match[0])
        result = await session.execute(query)
        user = result.scalars().first()
        if match[1] < LS_RATIO_MAX:
            user.is_bot = True
            await session.commit()
        return user


async def analyze_connection(fingerprint: FingerprintSchema, client_ip: str, long_hash: str, short_hash: str):
    base_score = 100
    language, timezone, is_mobile, is_proxy = utils.get_ip_external_data(client_ip)

    if fingerprint.timezone and not utils.is_valid_timezone(timezone, fingerprint.timezone.offset):
        base_score *= FP_RATIO.get("timezone", 1)
    if fingerprint.webRTC and not utils.is_valid_ip(client_ip, fingerprint.webRTC.value) or is_proxy:
        base_score *= FP_RATIO.get("webRTC", 1)
    if fingerprint.browser and not utils.is_valid_browser(fingerprint.browser):
        base_score *= FP_RATIO.get("browser", 1)
    if fingerprint.browser and not utils.is_valid_language(fingerprint.language, language):
        base_score *= FP_RATIO.get("language", 1)
    if fingerprint.UA and not fingerprint.UA or not fingerprint.UA.value:
        base_score *= FP_RATIO.get("UA", 1)
    if fingerprint.browser and fingerprint.browser.bot is True:
        base_score *= FP_RATIO.get("browser", 1)
    if fingerprint.browser and fingerprint.browser.driver is True:
        base_score *= FP_RATIO.get("browser", 1)
    if fingerprint.webGL and fingerprint.webGL.headless is True:
        base_score *= FP_RATIO.get("browser", 1)

    bot = base_score < LS_RATIO_MIN
    user = User(ip=fingerprint.webRTC.value or client_ip,
                uid=short_hash,
                hash=long_hash,
                fingerprint=fingerprint.json(),
                is_bot=bot)
    async with async_session_maker() as session:
        session.add(user)
        await session.commit()
        return user


async def async_celery_task(fingerprint: FingerprintSchema, client_ip: str):
    fingerprint = FingerprintSchema.parse_obj(fingerprint)
    to_hash = {}
    for k, v in fingerprint.dict().items():
        to_hash[k] = "".join([sha1(str(item).encode()).hexdigest()[:10] for key, item in v.items()])
    long_hash = "".join(
        [sha1(str(v).encode()).hexdigest()[:int(FP_PRIORITY.get(k, 1) * 10)] for k, v in to_hash.items()])
    short_hash = sha1(long_hash.encode()).hexdigest()
    user = await get_current_user(long_hash)
    if not user:
        user = await analyze_connection(fingerprint, client_ip, long_hash, short_hash)
    cookie = Cookie(user_id=user.id)
    async with async_session_maker() as session:
        session.add(cookie)
        await session.commit()
    return cookie.value


# @celery.task
async def analyze_fingerprint(fingerprint: FingerprintSchema, client_ip: str):
    result = await async_celery_task(fingerprint, client_ip)
    return result

    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(async_celery_task(fingerprint, client_ip))
    # return result
