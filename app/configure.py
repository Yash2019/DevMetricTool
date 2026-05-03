from pydantic_settings import BaseSettings, SettingsConfigDict

'''
Basesettings -> read env variable
SettingsConfigDict -> What to load
'''

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET: str

    model_config = SettingsConfigDict(
        env_file='app/.env',
        extra='ignore'
    )


config = Settings()