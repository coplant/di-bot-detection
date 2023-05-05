from babel import Locale
from datetime import datetime
import pytz
import requests

from proxy.src.service.schemas import BrowserSchema, LanguageSchema


def is_valid_language(fp_language: LanguageSchema, ip_language: str):
    if ip_language.lower() in fp_language.value[0].lower() or ip_language.lower() in fp_language.value[1].lower():
        return True
    return False


def is_valid_browser(browser: BrowserSchema):
    if browser.duck in browser.eval and browser.duck in browser.ua:
        return True
    return False


def get_ip_external_data(client_ip):
    url = f"http://ip-api.com/json/{client_ip}?fields=countryCode,timezone,mobile,proxy,query"
    response = requests.get(url).json()
    country_code = response.get("countryCode")
    language = Locale.parse(f"und_{country_code}").language
    timezone = response.get("timezone")
    is_mobile = response.get("mobile")
    is_proxy = response.get("proxy")
    return language, timezone, is_mobile, is_proxy


def is_valid_timezone(ip_timezone, fp_offset):
    pacific_now = datetime.now(pytz.timezone(ip_timezone))
    ip_offset = int(pacific_now.utcoffset().total_seconds() / 60)
    if abs(abs(ip_offset) - abs(fp_offset)) > 90:
        return False
    return True


def is_valid_ip(host_ip, fp_ip):
    if host_ip == fp_ip:
        return True
    return False
