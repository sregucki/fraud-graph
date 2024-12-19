from model.abc.entity import Entity
from model.device import Device

from data_generation.model.location import Location


class Account(Entity):
    def __init__(
        self, name: str, email: str, location: Location, device: Device = None
    ) -> None:
        super().__init__()
        self.name = name
        self.email = email
        self.device = device
        self.location = location

    def __str__(self):
        return f"Account: id={self.id} name={self.name} email={self.email} location={self.location} device={self.device}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.id == other.id

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "device_id": self.device.id if self.device else None,
            "country": self.location.country,
            "city": self.location.city,
            "street_address": self.location.street_address,
        }
