import mysql.connector
from mysql.connector import Error as MYSQLError
import os
import logging
from src.app.constants.database_config import DatabaseConfig
from src.app.constants.messages import LogMessages, ErrorMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MySQLConnector:
    """Manages MySQL database connections."""

    def __init__(self):
        """Initialize database connector with configuration parameters."""
        self.connection = None
        self.connection_parameters = {
            'host': os.getenv(DatabaseConfig.ENV_DB_HOST, DatabaseConfig.DEFAULT_HOST),
            'port': int(os.getenv(DatabaseConfig.ENV_DB_PORT, DatabaseConfig.DEFAULT_PORT)),
            'database': os.getenv(DatabaseConfig.ENV_DB_NAME, DatabaseConfig.DEFAULT_DATABASE),
            'user': os.getenv(DatabaseConfig.ENV_DB_USER, DatabaseConfig.DEFAULT_USER),
            'password': os.getenv(DatabaseConfig.ENV_DB_PASSWORD, DatabaseConfig.DEFAULT_PASSWORD)
        }

    def connect(self) -> None:
        """Establish connection to MySQL database."""
        if self.connection is not None and self.db_is_connected():
            logger.warning(LogMessages.DB_ALREADY_CONNECTED)
            return

        try:
            self.connection = mysql.connector.connect(**self.connection_parameters)
            self.connection.autocommit = True
            logger.info(LogMessages.DB_CONNECTED)
        except MYSQLError as error:
            logger.error(LogMessages.DB_CONNECTION_FAILED.format(error))
            raise
        except Exception as error:
            logger.error(LogMessages.DB_UNEXPECTED_CONNECTION_ERROR.format(error))
            raise

    def disconnect(self) -> None:
        """Close database connection."""
        if self.connection is None:
            return

        try:
            if self.connection.is_connected():
                self.connection.close()
                logger.info(LogMessages.DB_CONNECTION_CLOSED)
        except MYSQLError as e:
            logger.error(LogMessages.DB_DISCONNECT_FAILED.format(e))
        except Exception as e:
            logger.error(LogMessages.DB_UNEXPECTED_DISCONNECT_ERROR.format(e))
        finally:
            self.connection = None

    def db_is_connected(self) -> bool:
        """Check if database is connected."""
        try:
            return self.connection is not None and self.connection.is_connected()
        except (MYSQLError, Exception):
            return False

    def get_cursor(self, dictionary: bool = False):
        """Get database cursor for executing queries."""
        if not self.db_is_connected():
            logger.warning(LogMessages.DB_NOT_CONNECTED)
            raise ConnectionError(ErrorMessages.DB_NOT_CONNECTED)

        try:
            return self.connection.cursor(dictionary=dictionary)
        except MYSQLError as error:
            logger.error(LogMessages.DB_CURSOR_MYSQL_ERROR.format(error))
            raise
        except Exception as e:
            logger.error(LogMessages.DB_CURSOR_UNEXPECTED_ERROR.format(e))
            raise