from gino import Gino

from config import app_config

DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(
    app_config.db_user.get_secret_value(), app_config.db_password.get_secret_value(),
    app_config.db_host.get_secret_value(), app_config.db_port.get_secret_value(),
    app_config.db_name.get_secret_value(),
)

db = Gino()
