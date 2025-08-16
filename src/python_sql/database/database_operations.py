from abc import ABC, abstractmethod
from src.python_sql.database.database_connector import MySQLConnector, MYSQLError
from typing import Generator
from src.python_sql.constants.sql_queries import SQLQueries
from src.python_sql.constants.application_config import ApplicationConfig
from src.python_sql.constants.messages import LogMessages, ErrorMessages
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class EntityRepository(ABC):
    """Base class for database operations on entities."""

    def __init__(self, connector: MySQLConnector):
        """Initialize with database connector."""
        self.connector = connector
        self.batch_size = ApplicationConfig.DEFAULT_BATCH_SIZE

    @abstractmethod
    def insert_batch(self, items: Generator[dict, None, None]) -> None:
        """
        Inserts 1000 item at a time to the database

        :param items: Generator of item, for example, rooms, students.
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

    def execute_batch_insertion(self, items: Generator[dict, None, None]) -> None:
        """Execute batch insertion of items into database."""
        if not self.connector.db_is_connected():
            raise ConnectionError(ErrorMessages.DB_NOT_CONNECTED)

        cursor = self.connector.get_cursor()

        try:
            query = self.get_insert_query()
            batch = []

            for item in items:
                unpack_item = self.get_item_value(item)
                batch.append(unpack_item)

                if len(batch) >= self.batch_size:
                    cursor.executemany(query, batch)
                    logger.info(LogMessages.ITEMS_INSERTED.format(len(batch)))
                    batch = []

            if batch:
                cursor.executemany(query, batch)
                logger.info(LogMessages.FINAL_BATCH_INSERTED.format(len(batch)))

        except MYSQLError as error:
            logger.error(LogMessages.MYSQL_INSERTION_ERROR.format(error))
            raise
        except Exception as error:
            logger.error(LogMessages.UNEXPECTED_INSERTION_ERROR.format(error))
            raise
        finally:
            cursor.close()


class RoomRepository(EntityRepository):
    """Repository for room data operations."""

    def get_insert_query(self) -> str:
        """Get SQL query for room insertion."""
        return (
            SQLQueries.INSERT_ROOM_QUERY
        )

    def get_item_value(self, item: dict) -> tuple:
        """Extract room values from dictionary."""
        return item['id'], item['name']

    def insert_batch(self, rooms: Generator[dict, None, None]) -> None:
        """Insert batch of rooms into database."""
        self.execute_batch_insertion(rooms)
        logger.info(LogMessages.ROOM_INSERTION_COMPLETED)


class StudentRepository(EntityRepository):
    """Repository for student data operations."""

    def get_insert_query(self) -> str:
        """Get SQL query for student insertion."""
        return (
            SQLQueries.INSERT_STUDENT_QUERY
        )

    def get_item_value(self, item: dict) -> tuple:
        """Extract student values from dictionary."""
        return (
            item['id'],
            item['name'],
            item['birthday'],
            item['sex'],
            item['room']
        )

    def insert_batch(self, students: Generator[dict, None, None]) -> None:
        """Insert batch of students into database."""
        self.execute_batch_insertion(students)
        logger.info(LogMessages.STUDENT_INSERTION_COMPLETED)