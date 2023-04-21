from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from home.models import Code
from home.schemas import FormData


async def use_code(input_data: FormData, session: AsyncSession):
    code: str = input_data.code
    query = select(Code).filter_by(code=code)
    found_code = await session.execute(query)
    found_code = found_code.unique().scalar_one_or_none()
    if found_code:
        found_code.is_active = False
        await session.commit()
        return True
    return False
