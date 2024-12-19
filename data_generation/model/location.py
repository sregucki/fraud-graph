from data_generation.model.abc.entity import Entity


class Location(Entity):
    def __init__(self, country: str, city: str, street_address: str) -> None:
        super().__init__()
        self.country = country
        self.city = city
        self.street_address = street_address

    def __str__(self):
        return f"Location: country={self.country} city={self.city} street_address={self.street_address}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self) -> dict[str, str]:
        return {
            "country": self.country,
            "city": self.city,
            "street_address": self.street_address,
        }
