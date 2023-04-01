import configparser
from dataclasses import dataclass
import psycopg
from psycopg.rows import class_row
import jlc
import asyncpg

@dataclass
class JLCComponent(asyncpg.Record):
    name: str
    lcsc: str
    enabled: bool
    channel_id: int
    stock: int
    role_id: int = 0

    def __getattr__(self, name):
        return self[name]


@dataclass
class Database:

    def __enter__(self):
        config = configparser.ConfigParser()
        config.read("jlc.conf")
        self.__connection = psycopg.connect(
            config["postgres"]["database_url"],
        )
        return self

    def __exit__(self, type, value, traceback):
        self.__connection.close()

    def get_components(self):
        with self.__connection.cursor(row_factory=class_row(jlc.Component)) as cursor:
            cursor.execute("SELECT * FROM components;")
            return cursor.fetchall()

    def update_component(self, new_stock, lcsc):
        with self.__connection.cursor() as cursor:
            cursor.execute("UPDATE components SET stock = {} WHERE lcsc = '{}';".format(new_stock, lcsc))
            self.__connection.commit()

    def add_component(self, name, lcsc, channel):
        with self.__connection.cursor() as cursor:
            cursor.execute("INSERT INTO components (name, lcsc, enabled, channel_id, stock, role_id)\
             VALUES ('{}', '{}', {}, {}, {}, {})".format(name, lcsc, True, channel, 1, 0))
            self.__connection.commit()

CONFIG = configparser.ConfigParser()
CONFIG.read("jlc.conf")

if __name__ == "__main__":
    with Database() as db:
        print("xyz")  # implement something
