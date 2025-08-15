from typing import List, Dict, Any

from src.python_sql.database.repositories.base_repositories import RoomRepositoryInterface, StudentRepositoryInterface


class MySQLStudentRepository(StudentRepositoryInterface):
    def find_by_room_id(self, room_id: int) -> List[Dict[str, Any]] | None:
        pass

    def count_by_room_id(self, room_id: int) -> int:
        pass

    def insert(self, item: Dict[str, Any]) -> None:
        pass

    def insert_many(self, item_list: List[Dict[str, Any]]) -> None:
        pass

    def find_by_id(self, item_id: int) -> Dict[str, Any] | None:
        pass

    def find_all(self) -> List[Dict[str, Any]] | None:
        pass

    def exists(self, item_id: int) -> bool:
        pass

    def delete_by_id(self, item_id: int):
        pass


class MySQLRoomRepository(RoomRepositoryInterface):
    def insert(self, item: Dict[str, Any]) -> None:
        pass

    def insert_many(self, item_list: List[Dict[str, Any]]) -> None:
        pass

    def find_by_id(self, item_id: int) -> Dict[str, Any] | None:
        pass

    def find_all(self) -> List[Dict[str, Any]] | None:
        pass

    def exists(self, item_id: int) -> bool:
        pass

    def delete_by_id(self, item_id: int):
        pass
