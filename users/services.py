import asyncio

from asyncpg import UniqueViolationError

from db.models import User


async def create_user(tg_id: int, name: str) -> None:
    try:
        await User.create(tg_id=tg_id, name=name)
    except UniqueViolationError:
        # We don't have business logic for new or old user
        # This function will need to only user create, not more
        pass
    return


async def get_user(tg_id: int) -> User:
    user = await User.query.where(User.tg_id == tg_id).gino.scalar()
    return user
