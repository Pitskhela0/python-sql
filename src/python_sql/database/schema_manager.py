from database_connector import MySQLConnector
from mysql.connector import Error as MYSQLError
import logging

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class SchemaManager:
    def __init__(self, mysql_connector: MySQLConnector):
        self.connector = mysql_connector

    def create_room_student_schema(self):
        if not self.connector.db_is_connected():
            logger.error("Database not connected")
            raise ConnectionError("Database not connected")

        cursor = None
        try:
            cursor = self.connector.get_cursor()
            self._create_rooms_schema(cursor)
            self._create_students_schema(cursor)
            logger.info("Successfully created rooms and students schema")

        except MYSQLError as e:
            logger.error(f"MySQL error creating schema: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating schema: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def _create_rooms_schema(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rooms (
                room_id INT PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        logger.info("Rooms table created")

    def _create_students_schema(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                student_id INT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                birthday DATE NOT NULL,
                sex ENUM('M', 'F') NOT NULL,
                room_id INT,
                FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        logger.info("Students table created")

    def drop_rooms_students_schema(self):
        if not self.connector.db_is_connected():
            logger.error("Database not connected")
            raise ConnectionError("Database not connected")

        cursor = None
        try:
            cursor = self.connector.get_cursor()
            self._drop_students_table(cursor)
            self._drop_rooms_table(cursor)
            logger.info("Successfully dropped rooms and students schema")

        except MYSQLError as e:
            logger.error(f"MySQL error dropping schema: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error dropping schema: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def _drop_students_table(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS Students")
        logger.info("Students table dropped")

    def _drop_rooms_table(self, cursor):
        cursor.execute("DROP TABLE IF EXISTS Rooms")
        logger.info("Rooms table dropped")