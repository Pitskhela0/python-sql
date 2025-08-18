# test_basic.py
import unittest
from unittest.mock import Mock, patch
from src.app.services.data_validator import RoomValidator, StudentValidator, ValidatorContext
from src.app.services.data_filter import DataFilter
from src.app.database.database_operations import RoomRepository, StudentRepository


class TestValidators(unittest.TestCase):
    """Basic tests for data validation logic."""

    def setUp(self):
        self.room_validator = RoomValidator()
        self.student_validator = StudentValidator()

    def test_room_validator_valid_data(self):
        """Test room validator with valid data."""
        valid_room = {"id": 1, "name": "Room A"}
        self.assertTrue(self.room_validator.validate(valid_room))

    def test_room_validator_missing_fields(self):
        """Test room validator with missing required fields."""
        invalid_room = {"id": 1}  # missing name
        self.assertFalse(self.room_validator.validate(invalid_room))

    def test_room_validator_invalid_id(self):
        """Test room validator with invalid ID."""
        invalid_room = {"id": -1, "name": "Room A"}
        self.assertFalse(self.room_validator.validate(invalid_room))

    def test_room_validator_empty_name(self):
        """Test room validator with empty name."""
        invalid_room = {"id": 1, "name": ""}
        self.assertFalse(self.room_validator.validate(invalid_room))

    def test_student_validator_valid_data(self):
        """Test student validator with valid data."""
        valid_student = {
            "id": 1,
            "name": "John Doe",
            "birthday": "1995-05-15",
            "sex": "M",
            "room": 101
        }
        self.assertTrue(self.student_validator.validate(valid_student))

    def test_student_validator_missing_fields(self):
        """Test student validator with missing required fields."""
        invalid_student = {"id": 1, "name": "John Doe"}  # missing other fields
        self.assertFalse(self.student_validator.validate(invalid_student))

    def test_student_validator_invalid_room_id(self):
        """Test student validator with invalid room ID."""
        invalid_student = {
            "id": 1,
            "name": "John Doe",
            "birthday": "1995-05-15",
            "sex": "M",
            "room": -1  # invalid room ID
        }
        self.assertFalse(self.student_validator.validate(invalid_student))

    def test_validator_context_room(self):
        """Test validator context for room type."""
        context = ValidatorContext("room")
        valid_room = {"id": 1, "name": "Room A"}
        self.assertTrue(context.execute_validation(valid_room))

    def test_validator_context_invalid_type(self):
        """Test validator context with invalid type."""
        with self.assertRaises(ValueError):
            ValidatorContext("invalid_type")


class TestDataFilter(unittest.TestCase):
    """Basic tests for data filtering functionality."""

    @patch('src.app.services.data_filter.ValidatorContext')
    def test_filter_data_valid_items(self, mock_validator_context):
        """Test data filter with all valid items."""
        # Setup mock validator
        mock_validator = Mock()
        mock_validator.execute_validation.return_value = True
        mock_validator_context.return_value = mock_validator

        # Test data
        test_data = [{"id": 1, "name": "Room A"}, {"id": 2, "name": "Room B"}]

        # Filter data
        filtered_data = list(DataFilter.filter_data(iter(test_data), "room")) # type: ignore

        # Assertions
        self.assertEqual(len(filtered_data), 2)
        self.assertEqual(filtered_data, test_data)

    @patch('src.app.services.data_filter.ValidatorContext')
    def test_filter_data_mixed_validity(self, mock_validator_context):
        """Test data filter with mix of valid and invalid items."""
        # Setup mock validator to alternate between True/False
        mock_validator = Mock()
        mock_validator.execute_validation.side_effect = [True, False, True]
        mock_validator_context.return_value = mock_validator

        # Test data
        test_data = [
            {"id": 1, "name": "Room A"},  # valid
            {"id": -1, "name": ""},  # invalid
            {"id": 2, "name": "Room B"}  # valid
        ]

        # Filter data
        filtered_data = list(DataFilter.filter_data(iter(test_data), "room")) # type: ignore

        # Should only return valid items
        self.assertEqual(len(filtered_data), 2)
        self.assertEqual(filtered_data[0]["id"], 1)
        self.assertEqual(filtered_data[1]["id"], 2)


class TestRepositories(unittest.TestCase):
    """Basic tests for repository classes."""

    def setUp(self):
        self.mock_connector = Mock()
        self.mock_cursor = Mock()
        self.mock_connector.get_cursor.return_value = self.mock_cursor
        self.mock_connector.db_is_connected.return_value = True

    def test_room_repository_get_insert_query(self):
        """Test room repository returns correct insert query."""
        repo = RoomRepository(self.mock_connector)
        query = repo.get_insert_query()
        self.assertIn("INSERT INTO Rooms", query)
        self.assertIn("room_id, name", query)

    def test_room_repository_get_item_value(self):
        """Test room repository extracts correct values from item."""
        repo = RoomRepository(self.mock_connector)
        item = {"id": 1, "name": "Room A"}
        values = repo.get_item_value(item)
        self.assertEqual(values, (1, "Room A"))

    def test_student_repository_get_insert_query(self):
        """Test student repository returns correct insert query."""
        repo = StudentRepository(self.mock_connector)
        query = repo.get_insert_query()
        self.assertIn("INSERT INTO Students", query)
        self.assertIn("student_id, name, birthday, sex, room_id", query)

    def test_student_repository_get_item_value(self):
        """Test student repository extracts correct values from item."""
        repo = StudentRepository(self.mock_connector)
        item = {
            "id": 1,
            "name": "John Doe",
            "birthday": "1995-05-15",
            "sex": "M",
            "room": 101
        }
        values = repo.get_item_value(item)
        expected = (1, "John Doe", "1995-05-15", "M", 101)
        self.assertEqual(values, expected)

    def test_repository_connection_error(self):
        """Test repository raises error when database not connected."""
        self.mock_connector.db_is_connected.return_value = False
        repo = RoomRepository(self.mock_connector)

        with self.assertRaises(ConnectionError):
            repo.execute_batch_insertion(iter([]))  # type: ignore


if __name__ == '__main__':
    unittest.main()
