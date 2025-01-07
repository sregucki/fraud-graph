import pandas as pd

from model.abc.entity import Entity

from data_generation.log_collection.log_collector import collect_log


def write_to_csv(list_of_entities: list[Entity], filename: str) -> None:
    collect_log(f"Writing {len(list_of_entities)} entities to {filename}")
    pd.DataFrame([entity.to_dict() for entity in list_of_entities]).to_csv(
        f"../data/{filename}", index=False
    )
