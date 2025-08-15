from abc import ABC, abstractmethod
from typing import List, Dict, Any


class RepositoryInterface(ABC):
    @abstractmethod
    def insert(self, item: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def insert_many(self, item_list: List[Dict[str, Any]]) -> None:
        pass

    @abstractmethod
    def find_by_id(self, item_id: int) -> Dict[str, Any] | None:
        pass

    @abstractmethod
    def find_all(self) -> List[Dict[str, Any]] | None:
        pass

    @abstractmethod
    def exists(self, item_id: int) -> bool:
        pass

    @abstractmethod
    def delete_by_id(self, item_id: int):
        pass


class StudentRepositoryInterface(RepositoryInterface):
    @abstractmethod
    def find_by_room_id(self, room_id: int) -> List[Dict[str, Any]] | None:
        pass

    @abstractmethod
    def count_by_room_id(self, room_id: int) -> int:
        pass


class RoomRepositoryInterface(RepositoryInterface, ABC):
    pass

