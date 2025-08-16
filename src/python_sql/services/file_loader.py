from collections.abc import Generator
import ijson
from src.python_sql.constants.application_config import ApplicationConfig
from src.python_sql.constants.messages import ErrorMessages


class FileLoader:
    """Utility class for streaming JSON data from a file."""

    @staticmethod
    def load_file_data(path: str) -> Generator[dict, None, None]:
        """
        Stream JSON items from the given file one by one.

        Args:
            path: Path to the JSON file.
        Yields:
            dict: A JSON object parsed from the file.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If access to the file is denied.
            ValueError: If the file contains invalid JSON.
            OSError: If an unexpected I/O error occurs.
        """
        try:
            with open(path, ApplicationConfig.FILE_MODE_READ, encoding=ApplicationConfig.DEFAULT_ENCODING) as file:
                try:
                    yield from ijson.items(file, ApplicationConfig.JSON_ITEMS_PATH)
                except ijson.JSONError as e:
                    raise ValueError(ErrorMessages.INVALID_JSON_FORMAT.format(path)) from e
        except (FileNotFoundError, PermissionError):
            raise
        except OSError as e:
            raise OSError(ErrorMessages.FILE_READ_ERROR.format(path)) from e