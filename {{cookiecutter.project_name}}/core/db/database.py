{% if cookiecutter.database|lower() == 'n' %}
"""Don't use this code in production, this is just for JWT authentication works."""
import json
from pathlib import Path

DEFAULT_FAKEDB = (Path(__file__).parent.parent/"db"/"fakedb.json").resolve()

class FakeDataBase:

    def __init__(self, filepath:str=DEFAULT_FAKEDB):        
        self.filepath = filepath
        if not Path(self.filepath).exists():
            Path(self.filepath).touch()
        self._load()
    
    def _load(self):
        try:
            with open(self.filepath, "r") as f:
                self.data = json.load(f)
        except json.decoder.JSONDecodeError:
            self.data = []
    
    def get_user(self, login:str):
        try:
            if any(user["login"] == login for user in self.data):
                return next(user for user in self.data if user["login"] == login)
        except StopIteration:
            return None
        except KeyError:
            return None

    def check_exists_user(self, login:str):
        return any(user["login"] == login for user in self.data)
    
    def add_user(self, login:str, password:str):
        self.data.append({"login": login, "password": password})
        self._save()

    def get_password(self, login:str):
        return self.get_user(login)["password"]

    def _save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f)
{% else %}
from datetime import datetime
import logging
from core.settings import DATABASE_USER, DATABASE_PASSWORD
import pyodbc
from pyodbc import Connection, Cursor

logger = logging.getLogger(__name__)

class DataBaseConnection:
    def __init__(
        self,
        server: str = "localhost",
        database: str = "mydatabase",
        username: str = DATABASE_USER,
        password: str = DATABASE_PASSWORD,
        driver: str = "{SQL Server}",
        port: int = 3306,
    ):
        self._server = server
        self._database = database
        self._username = username
        self._password = password
        self._driver = driver
        self._port = port
        self.conn = None

    def __enter__(self):
        self.conn = pyodbc.connect(
            f"DRIVER={self._driver};"
            f"SERVER={self._server};"
            f"DATABASE={self._database};"
            f"UID={self._username};"
            f"PWD={self._password}"
        )
        cursor = self.conn.cursor()
        return self.Transaction(cursor, self.conn)

    def __exit__(self, *args):
        if self.conn:
            self.conn.close()
            self.conn = None

    class Transaction:
        def __init__(self, cursor: Cursor, conn: Connection):
            self.connection = conn
            self.cursor = cursor

        def execute(
            self,
            error_msg: str = None,
            cmd: str = None,
            is_fetch: bool = False,
        ):
            try:
                if is_fetch:
                    self.cursor.execute(cmd)
                    data = self.cursor.fetchall()
                    return data
                self.cursor.execute(cmd)
                self.cursor.commit()
            except Exception as er:
                if error_msg:
                    logger.error(f"{er} on query: {cmd} {error_msg}")
        
        def exists_user(self, username: str):
            cmd = f"select * from accounts where username = '{username}'"
            result = self.execute(cmd=cmd, error_msg="<- EXISTS USER", is_fetch=True)
            if result:
                return True
            return False

        def exists_user(self, username: str):
            cmd = f"select * from accounts where username = '{username}'"
            result = self.execute(cmd=cmd, error_msg="<- EXISTS USER", is_fetch=True)
            if result:
                return True
            return False

        def get_password(self, username: str):
            cmd = f"SELECT senhaUsuario FROM accounts where username = '{username}'"
            result = self.execute(
                cmd=cmd, error_msg="<- VERIFY CREDENTIALS", is_fetch=True
            )
            return result[0][0]

        def add_user(self, username: str, password: str, status: bool = True):
            cmd = f"insert into accounts (username, password, status, created_at, updated_at) values ('{username}', '{password}', '{status}', '{datetime.now()}', null)"
            self.execute(cmd=cmd, error_msg="<- ADD USER")

{% endif %}