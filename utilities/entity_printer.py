from model.abc.entity import Entity


def print_in_lines(l: list[Entity]) -> None:
    for entity in l:
        print(entity)
