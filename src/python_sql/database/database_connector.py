import mysql.connector
from mysql.connector import Error as MYSQLError
import os
import logging

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class MySQLConnector:
    def __init__(self):
        self.connection = None
        self.connection_parameters = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3307)),
            'database': os.getenv('DB_NAME', 'my_database'),
            'user': os.getenv('DB_USER', 'my_user'),
            'password': os.getenv('DB_PASSWORD', 'my_password')
        }

    def connect(self) -> None:
        if self.connection is not None and self.db_is_connected():
            logger.warning("Database is already connected")
            return

        try:
            self.connection = mysql.connector.connect(**self.connection_parameters)
            self.connection.autocommit = True
            logger.info("Connected to database")
        except MYSQLError as error:
            logger.error(f"Connection failed: {error}")
            raise
        except Exception as error:
            logger.error(f"Unexpected error while connecting to database: {error}")
            raise

    def disconnect(self) -> None:
        if self.connection is None:
            return

        try:
            if self.connection.is_connected():
                self.connection.close()
                logger.info("Database connection closed")
        except MYSQLError as e:
            logger.error(f"Failed to disconnect from database due to: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during disconnect: {e}")
        finally:
            self.connection = None

    def db_is_connected(self) -> bool:
        try:
            return self.connection is not None and self.connection.is_connected()
        except (MYSQLError, Exception):
            return False

    def get_cursor(self, dictionary: bool = False):
        if not self.db_is_connected():
            logger.warning("Database is not connected")
            raise ConnectionError("Database is not connected")

        try:
            return self.connection.cursor(dictionary=dictionary)
        except MYSQLError as error:
            logger.error(f"MySQL error getting cursor: {error}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting cursor: {e}")
            raise
