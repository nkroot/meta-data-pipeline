
from pydantic import BaseSettings

# Creating pydantic to capture the envionment variables

class Settings(BaseSettings):

    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    staging_schema:str
    development_schema:str
    retry:int
    sleep_time:int
    apikey:str
    class Config:
        env_file =".env"


settings = Settings()

