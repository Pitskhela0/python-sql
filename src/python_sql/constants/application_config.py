class ApplicationConfig:
    """Application-wide configuration constants"""

    ROOM_FILE_PATH = "src/resources/rooms.json"
    STUDENT_FILE_PATH = "src/resources/students.json"

    OUTPUT_DIR = "src/python_sql/output"
    TOP_5_LEAST_AVG_AGE_OUTPUT = f"{OUTPUT_DIR}/top_5_least_average_age_room.txt"
    ROOMS_WITH_DIFFERENT_SEX_OUTPUT = f"{OUTPUT_DIR}/rooms_with_different_sex.txt"
    ROOMS_WITH_STUDENTS_COUNT_OUTPUT = f"{OUTPUT_DIR}/rooms_with_students_count.txt"
    TOP_5_LARGEST_AGE_DIFF_OUTPUT = f"{OUTPUT_DIR}/top_5_rooms_with_largest_age_diff.txt"

    DEFAULT_BATCH_SIZE = 1000

    STUDENT_STRATEGY = "student"
    ROOM_STRATEGY = "room"

    DEFAULT_ENCODING = "utf-8"
    FILE_MODE_WRITE = "w"
    FILE_MODE_READ = "r"

    JSON_ITEMS_PATH = "item"
