from src.app.database.database_connector import MySQLConnector
from src.app.constants.sql_queries import SQLQueries


class ReportingService:
    """Service for generating reports from database queries."""

    def __init__(self, db_connection: MySQLConnector):
        """Initialize with database connection."""
        self.connector = db_connection

    def rooms_with_students_count(self):
        """Get count of students in each room."""
        cursor = self.connector.get_cursor(dictionary=True)
        cursor.execute(
            SQLQueries.ROOMS_WITH_STUDENTS_COUNT
        )

        return cursor.fetchall()

    def top_5_least_average_age_room(self):
        """Get top 5 rooms with lowest average age."""
        cursor = self.connector.get_cursor(dictionary=True)
        cursor.execute(
            SQLQueries.TOP_5_LEAST_AVERAGE_AGE_ROOMS
        )

        return cursor.fetchall()

    def top_5_rooms_with_largest_age_diff(self):
        """Get top 5 rooms with largest age difference between students."""
        cursor = self.connector.get_cursor(dictionary=True)
        cursor.execute(
            SQLQueries.TOP_5_LARGEST_AGE_DIFF_ROOMS
        )

        return cursor.fetchall()

    def rooms_with_different_sex(self):
        """Get rooms that have both male and female students."""
        cursor = self.connector.get_cursor(dictionary=True)
        cursor.execute(
            SQLQueries.ROOMS_WITH_DIFFERENT_SEX
        )

        return cursor.fetchall()