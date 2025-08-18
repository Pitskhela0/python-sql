from src.app.database.database_connector import MySQLConnector
from mysql.connector import Error as MYSQLError
from src.app.constants.sql_queries import SQLQueries
from src.app.constants.messages import LogMessages, ErrorMessages
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _drop_rooms_table(cursor):
    """Drop the rooms table from database."""
    cursor.execute(SQLQueries.DROP_ROOMS_TABLE)
    logger.info(LogMessages.ROOMS_TABLE_DROPPED)


def _drop_students_table(cursor):
    """Drop the students table from database."""
    cursor.execute(SQLQueries.DROP_STUDENTS_TABLE)
    logger.info(LogMessages.STUDENTS_TABLE_DROPPED)


def _create_students_schema(cursor):
    """Create the students table in database."""
    cursor.execute(
        SQLQueries.CREATE_STUDENTS_TABLE
    )
    logger.info(LogMessages.STUDENTS_TABLE_CREATED)


def _create_rooms_schema(cursor):
    """Create the rooms table in database."""
    cursor.execute(
        SQLQueries.CREATE_ROOMS_TABLE
    )
    logger.info(LogMessages.ROOMS_TABLE_CREATED)


class SchemaManager:
    """Manages database schema operations for rooms and students tables."""

    def __init__(self, mysql_connector: MySQLConnector):
        """Initialize with database connector."""
        self.connector = mysql_connector

    def create_room_student_schema(self):
        """Create both rooms and students tables."""
        if not self.connector.db_is_connected():
            logger.error(LogMessages.DB_NOT_CONNECTED)
            raise ConnectionError(ErrorMessages.DB_NOT_CONNECTED)

        cursor = None
        try:
            cursor = self.connector.get_cursor()
            _create_rooms_schema(cursor)
            _create_students_schema(cursor)
            logger.info(LogMessages.SCHEMA_CREATED_SUCCESS)

        except MYSQLError as e:
            logger.error(LogMessages.SCHEMA_MYSQL_ERROR_CREATE.format(e))
            raise
        except Exception as e:
            logger.error(LogMessages.SCHEMA_UNEXPECTED_ERROR_CREATE.format(e))
            raise
        finally:
            if cursor:
                cursor.close()

    def drop_rooms_students_schema(self):
        """Drop both rooms and students tables."""
        if not self.connector.db_is_connected():
            logger.error(LogMessages.DB_NOT_CONNECTED)
            raise ConnectionError(ErrorMessages.DB_NOT_CONNECTED)

        cursor = None
        try:
            cursor = self.connector.get_cursor()
            _drop_students_table(cursor)
            _drop_rooms_table(cursor)
            logger.info(LogMessages.SCHEMA_DROPPED_SUCCESS)

        except MYSQLError as e:
            logger.error(LogMessages.SCHEMA_MYSQL_ERROR_DROP.format(e))
            raise
        except Exception as e:
            logger.error(LogMessages.SCHEMA_UNEXPECTED_ERROR_DROP.format(e))
            raise
        finally:
            if cursor:
                cursor.close()