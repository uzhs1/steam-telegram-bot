from gino import Gino

from config import config

# postgresql://{db_data.user}:{db_data.password}@{db_data.host}:{db_data.port}
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(
    config.db_user.get_secret_value(), config.db_password.get_secret_value(),
    config.db_host.get_secret_value(), config.db_port.get_secret_value(),
    config.db_name.get_secret_value(),
)

db = Gino()


async def create_tables() -> None:
    await db.set_bind(DATABASE_URL)
    await db.gino.create_all()


# Disconnected from db == await db.pop_bind().close()
