from src.python_sql.database.database_connector import MySQLConnector


class ReportingService:
    def __init__(self, db_connection: MySQLConnector):
        self.connector = db_connection

    def rooms_with_students_count(self):
        cursor = self.connector.get_cursor()
        cursor.execute(
            """
            SELECT Rooms.room_id, Rooms.name, count(Students.student_id) AS students_count
            FROM Rooms
            LEFT JOIN Students
            ON Rooms.room_id = Students.room_id
            GROUP BY Rooms.room_id;
            """
        )

        return cursor.fetchall()

    def top_5_least_average_age_room(self):
        cursor = self.connector.get_cursor()
        cursor.execute("""
        SELECT
            Rooms.room_id,
            Rooms.name,
            AVG(FLOOR(DATEDIFF(CURDATE(), Students.birthday) / 365.25)) AS avg_age
        FROM Rooms
        INNER JOIN Students ON Rooms.room_id = Students.room_id
        GROUP BY Rooms.room_id
        ORDER BY avg_age ASC
        LIMIT 5;
        """)

        return cursor.fetchall()

    def top_5_rooms_with_largest_age_diff(self):
        cursor = self.connector.get_cursor()
        cursor.execute("""
        SELECT
            Rooms.room_id,
            Rooms.name,
            MAX(TIMESTAMPDIFF(YEAR, Students.birthday, CURDATE())) -
            MIN(TIMESTAMPDIFF(YEAR, Students.birthday, CURDATE())) AS age_diff
        FROM Rooms
        INNER JOIN Students
            ON Rooms.room_id = Students.room_id
        GROUP BY Rooms.room_id, Rooms.name
        ORDER BY age_diff DESC
        LIMIT 5;
        """)

        return cursor.fetchall()

    def rooms_with_different_sex(self):
        cursor = self.connector.get_cursor()
        cursor.execute("""
                SELECT
                    Rooms.room_id,
                    Rooms.name
                FROM Rooms
                INNER JOIN Students
                    ON Rooms.room_id = Students.room_id
                GROUP BY Rooms.room_id
                HAVING COUNT(DISTINCT Students.sex) > 1;
                """)

        return cursor.fetchall()
