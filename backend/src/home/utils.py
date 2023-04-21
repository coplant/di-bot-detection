from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from home.models import Code
from home.schemas import FormData


async def get_code(input_data: FormData, session: AsyncSession):
    code: str = input_data.code
    query = select(Code).filter_by(code=code).filter_by(is_active=True)
    found_code = await session.execute(query)
    return found_code.unique().scalar_one_or_none()
