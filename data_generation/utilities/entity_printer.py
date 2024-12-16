from model.abc.entity import Entity


def print_in_lines(list_of_entities: list[Entity]) -> None:
    for entity in list_of_entities:
        print(entity)
