from abc import ABC, abstractmethod
from src.python_sql.database.database_connector import MySQLConnector
from typing import Generator, Optional
import logging

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class EntityRepository(ABC):

    def __init__(self, connector: MySQLConnector):
        self.connector = connector
        self.batch_size = 1000

    @abstractmethod
    def insert_batch(self, items: Generator[dict, None, None]) -> None:
        """
        Inserts 1000 item at a time to the database

        :param items: Generator of item, for example, rooms, students..
        :return: None
        """
        pass

    @abstractmethod
    def get_insert_query(self) -> str:
        """
        Returns query of insertion

        :return: String
        """
        pass

    @abstractmethod
    def get_item_value(self, item: dict) -> tuple:
        """
        Unpacks the dictionary values into tuple and
        returns in order for insertion

        :param item: Dictionary item from generator
        :return: Ordered data of dictionary
        """
        pass

    def execute_batch_insertion(self, items: Generator[dict, None, None]):
        if not self.connector.db_is_connected():
            raise ConnectionError("DB not connected")

        cursor = self.connector.get_cursor()

        try:
            query = self.get_insert_query()
            batch: list[Optional[tuple]] = [None] * self.batch_size

            count = 0
            for item in items:
                unpack_item = self.get_item_value(item)
                batch[count] = unpack_item
                count += 1

                if count >= self.batch_size:
                    cursor.executemany(query, batch)
                    logger.info(f"Inserted {len(batch)} items")
                    batch.clear()

            if len(batch) > self.batch_size:
                cursor.executemany(query, batch)
                logger.info(f"Inserted {len(batch)} items")
                batch.clear()

        except Exception as error:
            logger.warning(f"Unable to finish insertion: {error}")
        finally:
            cursor.close()


class RoomRepository(EntityRepository):
    def get_insert_query(self) -> str:
        return (
            """
            INSERT INTO Rooms (room_id, name)
            VALUES (%s, %s)
            """
        )

    def get_item_value(self, item: dict) -> tuple:
        return item['id'], item['name']

    def insert_batch(self, rooms: Generator[dict, None, None]) -> None:
        self.execute_batch_insertion(rooms)


class StudentRepository(EntityRepository):
    def get_insert_query(self) -> str:
        return (
            """
            INSERT INTO Students (student_id, name, birthday, sex, room_id)
            VALUES (%s, %s, %s, %s, %s)
            """
        )

    def get_item_value(self, item: dict) -> tuple:
        return (
            item['id'],
            item['name'],
            item['birthday'],
            item['sex'],
            item['room_id']
        )

    def insert_batch(self, students: Generator[dict, None, None]) -> None:
        self.execute_batch_insertion(students)
