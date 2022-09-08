{% if cookiecutter.database|lower() == 'y' %}
from .database import DataBaseConnection as DataBase
{% else %}
from .database import FakeDataBase as DataBase
{% endif %}