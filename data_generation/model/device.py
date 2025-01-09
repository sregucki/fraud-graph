from model.abc.entity import Entity


class Device(Entity):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Device: id={self.id}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self) -> dict[str, str]:
        return {"id": self.id, "name": self.name}
