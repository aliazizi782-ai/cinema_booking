from dbutils.pooled_db import PooledDB
import pymysql
from contextlib import contextmanager

class DatabasePool:
    _pool = None

    @classmethod
    def initialize(cls, host="127.0.0.1", user="root", password="root", 
                   database="cinema_booking", max_connections=5):
        """Creating connection pool """
        if cls._pool is None:
            cls._pool = PooledDB(
                creator=pymysql,
                maxconnections=max_connections,
                mincached=2,
                maxcached=5,
                blocking=True,
                host=host,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4'
            )

    @classmethod
    def get_temp_connection(cls, host="127.0.0.1", user="root", password="root"):
        """ Creating temp connection without create DB"""
        return pymysql.connect(
            host=host,
            user=user,
            password=password,
            charset='utf8mb4'
        )

    @classmethod
    @contextmanager
    def get_connection(cls):
        connection = cls._pool.connection()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @classmethod
    @contextmanager
    def get_cursor(cls):
        with cls.get_connection() as connection:
            cursor = connection.cursor()
            try:
                yield cursor
            finally:
                cursor.close()