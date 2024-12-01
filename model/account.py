from model.abc.entity import Entity
from model.device import Device


class Account(Entity):
    def __init__(self, name: str, email: str, device: Device = None) -> None:
        super().__init__()
        self.name = name
        self.email = email
        self.device = device

    def __str__(self):
        return f"Account: id={self.id} name={self.name} email={self.email}, device={self.device}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id
