from typing import List


class Data:
    id: str
    pack_count: int = 0
    inventory: List[int] = []

    def __init__(self, id: str) -> None:
        self.id = id

    def __str__(self) -> str:
        return self.id
