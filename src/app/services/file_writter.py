import os
import logging
from typing import List, Dict
from src.app.constants.application_config import ApplicationConfig
from src.app.constants.messages import LogMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ResultWriter:
    """Writes query results to text files."""

    @staticmethod
    def write_txt(file_path: str, data: List[Dict]):
        """
        Write a list of dictionaries to a plain text file.
        """
        if not data:
            logger.warning(LogMessages.NO_DATA_TO_WRITE.format(file_path))
            return

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, mode=ApplicationConfig.FILE_MODE_WRITE, encoding=ApplicationConfig.DEFAULT_ENCODING) as f:
                for row in data:
                    line = ", ".join(f"{k}: {v}" for k, v in row.items())
                    f.write(line + "\n")
            logger.info(LogMessages.FILE_WRITE_SUCCESS.format(len(data), file_path))
        except Exception as e:
            logger.error(LogMessages.FILE_WRITE_FAILED.format(file_path, e))
            raise