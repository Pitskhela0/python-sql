import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ResultWriter:
    @staticmethod
    def write_txt(file_path: str, data: List[Dict]):
        """
        Write a list of dictionaries to a plain text file.
        """
        if not data:
            logger.warning(f"No data to write for file: {file_path}")
            return

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, mode="w", encoding="utf-8") as f:
                for row in data:
                    line = ", ".join(f"{k}: {v}" for k, v in row.items())
                    f.write(line + "\n")
            logger.info(f"Successfully wrote {len(data)} rows to {file_path}")
        except Exception as e:
            logger.error(f"Failed to write to {file_path}: {e}")
            raise
