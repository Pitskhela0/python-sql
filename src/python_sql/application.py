from src.python_sql.services.file_loader import FileLoader
from src.python_sql.services.data_filter import DataFilter
from src.python_sql.database.database_connector import MySQLConnector
from src.python_sql.database.schema_manager import SchemaManager
from src.python_sql.database.database_operations import RoomRepository, StudentRepository
from src.python_sql.services.reporting_service import ReportingService
from src.python_sql.services.file_writter import ResultWriter
from src.python_sql.constants.application_config import ApplicationConfig

from typing import Final
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

room_file: Final = ApplicationConfig.ROOM_FILE_PATH
student_file: Final = ApplicationConfig.STUDENT_FILE_PATH


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
        # load data from json
        rooms = DataFilter.filter_data(FileLoader.load_file_data(room_file), ApplicationConfig.ROOM_STRATEGY)
        students = DataFilter.filter_data(FileLoader.load_file_data(student_file), ApplicationConfig.STUDENT_STRATEGY)

        # connect to database
        db_connection = MySQLConnector()
        db_connection.connect()

        # create schema
        schema_manager = SchemaManager(db_connection)
        schema_manager.create_room_student_schema()

        # insert data
        rooms_repo = RoomRepository(db_connection)
        rooms_repo.insert_batch(rooms)

        students_repo = StudentRepository(db_connection)
        students_repo.insert_batch(students)

        # do report
        report = ReportingService(db_connection)

        # write report
        ResultWriter.write_txt(ApplicationConfig.TOP_5_LEAST_AVG_AGE_OUTPUT, report.top_5_least_average_age_room())

        ResultWriter.write_txt(ApplicationConfig.ROOMS_WITH_DIFFERENT_SEX_OUTPUT, report.rooms_with_different_sex())

        ResultWriter.write_txt(ApplicationConfig.ROOMS_WITH_STUDENTS_COUNT_OUTPUT, report.rooms_with_students_count())

        ResultWriter.write_txt(ApplicationConfig.TOP_5_LARGEST_AGE_DIFF_OUTPUT, report.top_5_rooms_with_largest_age_diff())

    except Exception as e:
        print(e)