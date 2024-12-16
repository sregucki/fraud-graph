from abc import ABC, abstractmethod

import shortuuid


class Entity(ABC):
    def __init__(self):
        self.id = shortuuid.uuid()

    @abstractmethod
    def to_dict(self) -> dict[str, str]:
        pass
