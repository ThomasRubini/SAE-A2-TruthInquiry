import os

from sqlalchemy import engine as eg

def get_db_url():
       return eg.URL.create(
            "mariadb+pymysql",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_DBNAME")
        )