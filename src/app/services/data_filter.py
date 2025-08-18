import logging
from typing import Generator
from src.app.services.data_validator import ValidatorContext
from src.app.constants.messages import LogMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DataFilter:
    """Filters data by validating each item and keeping only the valid ones."""

    @staticmethod
    def filter_data(
        data: Generator[dict, None, None], data_type: str
    ) -> Generator[dict, None, None]:
        """
        Takes data items one by one and only returns the valid ones.

        Args:
            data: Stream of data items to check
            data_type: What kind of data we're checking ('student' or 'room')

        Returns:
            Only the valid data items
        """
        validation_context = ValidatorContext(data_type)
        for item in data:
            if validation_context.execute_validation(item):
                yield item
            else:
                logger.warning(LogMessages.SKIPPING_INVALID_ITEM.format(item))