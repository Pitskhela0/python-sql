from src.python_sql.database.database_connector import MySQLConnector
from src.python_sql.constants.sql_queries import SQLQueries


class ReportingService:
    def __init__(self, db_connection: MySQLConnector):
        self.connector = db_connection

    def rooms_with_students_count(self):
        cursor = self.connector.get_cursor(dictionary=True)
        cursor.execute(
            SQLQueries.ROOMS_WITH_STUDENTS_COUNT
        )

        return cursor.fetchall()

    def top_5_least_average_age_room(self):
        cursor = self.connector.get_cursor(dictionary=True)
        cursor.execute(
            SQLQueries.TOP_5_LEAST_AVERAGE_AGE_ROOMS
        )

        return cursor.fetchall()

    def top_5_rooms_with_largest_age_diff(self):
        cursor = self.connector.get_cursor(dictionary=True)
        cursor.execute(
            SQLQueries.TOP_5_LARGEST_AGE_DIFF_ROOMS
        )

        return cursor.fetchall()

    def rooms_with_different_sex(self):
        cursor = self.connector.get_cursor(dictionary=True)
        cursor.execute(
            SQLQueries.ROOMS_WITH_DIFFERENT_SEX
        )

        return cursor.fetchall()
