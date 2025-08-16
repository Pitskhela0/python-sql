class LogMessages:
    """Centralized log messages for the application"""

    # Database Connection Messages
    DB_ALREADY_CONNECTED = "Database is already connected"
    DB_CONNECTED = "Connected to database"
    DB_CONNECTION_FAILED = "Connection failed: {}"
    DB_UNEXPECTED_CONNECTION_ERROR = "Unexpected error while connecting to database: {}"
    DB_CONNECTION_CLOSED = "Database connection closed"
    DB_DISCONNECT_FAILED = "Failed to disconnect from database due to: {}"
    DB_UNEXPECTED_DISCONNECT_ERROR = "Unexpected error during disconnect: {}"
    DB_NOT_CONNECTED = "Database is not connected"
    DB_CURSOR_MYSQL_ERROR = "MySQL error getting cursor: {}"
    DB_CURSOR_UNEXPECTED_ERROR = "Unexpected error getting cursor: {}"

    ROOMS_TABLE_DROPPED = "Rooms table dropped"
    STUDENTS_TABLE_DROPPED = "Students table dropped"
    STUDENTS_TABLE_CREATED = "Students table created"
    ROOMS_TABLE_CREATED = "Rooms table created"
    SCHEMA_CREATED_SUCCESS = "Successfully created rooms and students schema"
    SCHEMA_DROPPED_SUCCESS = "Successfully dropped rooms and students schema"
    SCHEMA_MYSQL_ERROR_CREATE = "MySQL error creating schema: {}"
    SCHEMA_MYSQL_ERROR_DROP = "MySQL error dropping schema: {}"
    SCHEMA_UNEXPECTED_ERROR_CREATE = "Unexpected error creating schema: {}"
    SCHEMA_UNEXPECTED_ERROR_DROP = "Unexpected error dropping schema: {}"

    ITEMS_INSERTED = "Inserted {} items"
    FINAL_BATCH_INSERTED = "Inserted final batch of {} items"
    MYSQL_INSERTION_ERROR = "MySQL error during insertion: {}"
    UNEXPECTED_INSERTION_ERROR = "Unexpected error during insertion: {}"
    ROOM_INSERTION_COMPLETED = "Room insertion completed"
    STUDENT_INSERTION_COMPLETED = "inserted in students"

    SKIPPING_INVALID_ITEM = "skipping {}"
    ROOM_VALIDATION_FAILED = "Room validation failed {}"
    STUDENT_VALIDATION_FAILED = "Student validation failed: {}"

    NO_DATA_TO_WRITE = "No data to write for file: {}"
    FILE_WRITE_SUCCESS = "Successfully wrote {} rows to {}"
    FILE_WRITE_FAILED = "Failed to write to {}: {}"


class ErrorMessages:
    """Centralized error messages for the application"""

    APPLICATION_FAILURE = "Application failed"
    DB_NOT_CONNECTED = "Database is not connected"
    ROOM_DATA_INCOMPLETE = "Room data is incomplete"
    STUDENT_DATA_INCOMPLETE = "Student data is incomplete"
    INVALID_ROOM_ID = "Room ID must be positive integer, got: {}"
    INVALID_ROOM_NAME = "Room name must be non-empty string, got: {}"
    INVALID_STUDENT_ID = "Student ID must be positive integer, got: {}"
    INVALID_STUDENT_NAME = "Student name must be non-empty string, got: {}"
    INVALID_STUDENT_ROOM_ID = "Room ID must be positive integer, got: {}"
    UNKNOWN_STRATEGY_TYPE = "{} is unknown to the application"
    INVALID_JSON_FORMAT = "Invalid JSON format in file: {}"
    FILE_READ_ERROR = "Error reading file: {}"
