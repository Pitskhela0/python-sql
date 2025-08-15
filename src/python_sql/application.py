from src.python_sql.services.file_loader import FileLoader
from src.python_sql.services.data_filter import DataFilter
from src.python_sql.database.database_connector import MySQLConnector
from src.python_sql.database.schema_manager import SchemaManager
from src.python_sql.database.database_operations import RoomRepository, StudentRepository
from src.python_sql.services.reporting_service import ReportingService
from src.python_sql.services.file_writter import ResultWriter

from typing import Final
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

room_file: Final = "src/resources/rooms.json"
student_file: Final = "src/resources/students.json"


def start_application() -> None:
    """
    Application flow logic:
    1. Load data from both files
    2. Create database schema
    3. Insert data into database
    4. Retrieve data using SQL queries
    :return: None
    """

    try:

        rooms = DataFilter.filter_data(FileLoader.load_file_data(room_file), "room")
        students = DataFilter.filter_data(FileLoader.load_file_data(student_file), "student")


        # connect to database
        db_connection = MySQLConnector()
        db_connection.connect()

        # create schema
        schema_manager = SchemaManager(db_connection)
        schema_manager.create_room_student_schema()
        print("schema created")

        # insert data
        rooms_repo = RoomRepository(db_connection)
        rooms_repo.insert_batch(rooms)

        students_repo = StudentRepository(db_connection)
        students_repo.insert_batch(students)

        report = ReportingService(db_connection)

        ResultWriter.write_txt("src/python_sql/output/top_5_least_average_age_room.txt", report.top_5_least_average_age_room())

        ResultWriter.write_txt("src/python_sql/output/rooms_with_different_sex.txt", report.rooms_with_different_sex())

        ResultWriter.write_txt("src/python_sql/output/rooms_with_students_count.txt", report.rooms_with_students_count())

        ResultWriter.write_txt("src/python_sql/output/top_5_rooms_with_largest_age_diff.txt", report.top_5_rooms_with_largest_age_diff())

    except Exception as e:
        print(e)
