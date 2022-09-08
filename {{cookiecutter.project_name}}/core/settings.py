import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 0)) or 30
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
HEADER_TYPE = os.getenv('HEADER_TYPE','Bearer')
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES', 0)) or 60 * 24
SECRET_KEY = os.getenv('SECRET_KEY','SECRET KEY')

{% if cookiecutter.database|lower() == 'y' %}
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
{% endif %}
