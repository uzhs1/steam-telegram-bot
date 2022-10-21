from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    # Bot data
    bot_token: SecretStr

    # Database data
    db_user: SecretStr
    db_password: SecretStr
    db_name: SecretStr
    db_host: SecretStr
    db_port: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
