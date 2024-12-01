from abc import ABC

import shortuuid


class Entity(ABC):
    def __init__(self):
        self.id = shortuuid.uuid()
