import configparser
from dataclasses import dataclass
import psycopg
from psycopg.rows import class_row
import jlc

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
            cursor.execute("UPDATE components SET stock = {} WHERE lcsc={};".format(new_stock, lcsc))


CONFIG = configparser.ConfigParser()
CONFIG.read("jlc.conf")

if __name__ == "__main__":
    with Database() as db:
        print("xyz")  # implement something
