
import sqlite3
from loguru import logger
from bot.config import settings

class Manager:
    """Class for managing database connection and data"""

    def __init__(self) -> None:
        """Initialize database connection and create table if not exists"""

        self.connection = sqlite3.connect(settings.DATA / "car.db")
        self.create_table()

    def create_table(self) -> None:
        """Create table if not exists"""

        cursor = self.connection.cursor()
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS car_data (
                url TEXT,
                title TEXT,
                price_usd TEXT,
                distance TEXT,
                town TEXT,
                image_url_1 TEXT,
                image_url_2 TEXT,
                image_url_3 TEXT,
                image_url_4 TEXT,
                image_url_5 TEXT
            );
        """
        cursor.execute(create_table_sql)
        self.connection.commit()
        cursor.close()

        logger.info("Table created")

    def insert_data(self, values: list[tuple]) -> None:
        """Insert data into table
        :param values: list of tuples with data
        """

        cursor = self.connection.cursor()
        cursor.executemany(
            "INSERT INTO car_data (url, title, price_usd, distance, town, image_url_1, image_url_2, image_url_3, image_url_4, image_url_5) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            values,
        )
        self.connection.commit()
        cursor.close()

        logger.info("Data inserted")
        
    def select_data(self) -> list[tuple]:
        """Select data from table
        :return: list of tuples with data"""

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM car_data")
        data = cursor.fetchall()
        cursor.close()

        logger.info("Data selected")

        return data
    
    def delete_data(self, data: list[tuple]) -> None:
        """Delete data from table
        :param data: list of tuples with data
        """
        data = [(url[0],) for url in data]
        cursor = self.connection.cursor()
        cursor.executemany("DELETE FROM car_data WHERE url=?", data) # TODO check if it works
        self.connection.commit()
        cursor.close()
        
        logger.info("Data deleted")
        
    def change_price_data(self, data: list[tuple]) -> None:
        """Update data in table
        :param data: list of tuples with data
        """
        data = [(price[2], price[0]) for price in data]
        cursor = self.connection.cursor()
        cursor.executemany("UPDATE car_data SET price_usd=? WHERE url=?", data)
        self.connection.commit()
        cursor.close()
        
        logger.info("Data updated")