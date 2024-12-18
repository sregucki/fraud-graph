import pandas as pd

from model.abc.entity import Entity


def write_to_csv(list_of_entities: list[Entity], filename: str) -> None:
    pd.DataFrame([entity.to_dict() for entity in list_of_entities]).to_csv(
        f"../data/{filename}", index=False
    )
