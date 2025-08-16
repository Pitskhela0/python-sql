import logging
from abc import ABC, abstractmethod
from typing import Any, Dict
from src.python_sql.constants.messages import LogMessages, ErrorMessages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ValidationStrategy(ABC):
    """Base class for all validators.
    Each validator checks different types of data."""

    @abstractmethod
    def validate(self, item: Dict[str, Any]) -> bool:
        """Check if a data item is valid. Return True if good, False if bad."""
        pass


class RoomValidator(ValidationStrategy):
    """Checks if room data is correct and complete."""

    def validate(self, item: dict) -> bool:
        """
        Makes sure a room has valid ID and name.

        A valid room must have:
        - An 'id' that's a positive number
        - A 'name' that's not empty
        """
        try:
            if "id" not in item or "name" not in item:
                raise ValueError(ErrorMessages.ROOM_DATA_INCOMPLETE)

            room_id, room_name = item["id"], item["name"]

            if not isinstance(room_id, int) or room_id < 0:
                raise ValueError(ErrorMessages.INVALID_ROOM_ID.format(room_id))

            if not isinstance(room_name, str) or not room_name.strip():
                raise ValueError(ErrorMessages.INVALID_ROOM_NAME.format(room_name))

            return True
        except Exception as e:
            logger.error(LogMessages.ROOM_VALIDATION_FAILED.format(e))
            return False


class StudentValidator(ValidationStrategy):
    """Checks if student data is correct and complete."""

    def validate(self, item: dict) -> bool:
        """
        Makes sure a student has valid ID, name, and room assignment.

        A valid student must have:
        - An 'id' that's a positive number
        - A 'name' that's not empty
        - A 'room' that's a positive number
        """
        try:
            if ("id" not in item
                    or "name" not in item
                    or "room" not in item
                    or "birthday" not in item
                    or "sex" not in item
            ):
                raise ValueError(ErrorMessages.STUDENT_DATA_INCOMPLETE)

            student_id, student_name, room_id, student_birthday, student_sex\
                = (item["id"], item["name"], item["room"], item["birthday"], item["sex"])

            if not isinstance(student_id, int) or student_id < 0:
                raise ValueError(ErrorMessages.INVALID_STUDENT_ID.format(student_id))

            if not isinstance(student_name, str) or not student_name.strip():
                raise ValueError(ErrorMessages.INVALID_STUDENT_NAME.format(student_name))

            if not isinstance(room_id, int) or room_id < 0:
                raise ValueError(ErrorMessages.INVALID_STUDENT_ROOM_ID.format(room_id))

            return True

        except Exception as e:
            logger.error(LogMessages.STUDENT_VALIDATION_FAILED.format(e))
            return False


class ValidatorContext:
    """Picks the right validator for the type of data you're checking."""

    _strategies = {"student": StudentValidator, "room": RoomValidator}

    def __init__(self, strategy_type: str):
        """
        Set up the validator for a specific data type.

        Args:
            strategy_type: Either 'student' or 'room'
        """
        if strategy_type not in self._strategies:
            raise ValueError(ErrorMessages.UNKNOWN_STRATEGY_TYPE.format(strategy_type))
        self.strategy = self._strategies[strategy_type]()

    def execute_validation(self, item: dict) -> bool:
        """Check if the item is valid using the right validator."""
        return self.strategy.validate(item)