from datetime import timedelta

from pydantic import BaseModel


# Default Auth Settings class
class SettingsJWT(BaseModel):
    authjwt_secret_key: str
    authjwt_algorithm: str
    authjwt_access_token_expires: timedelta = timedelta(minutes=30)
    authjwt_refresh_token_expires: timedelta = timedelta(days=1)
    authjwt_header_type: str = "Bearer"

# Default User
class User(BaseModel):
    username: str
    password: str

# Write your models here
