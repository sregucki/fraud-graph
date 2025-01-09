import random

from data_generation.model.device import Device

brands = [
    "Dell",
    "HP",
    "Lenovo",
    "Samsung",
    "Apple",
    "Asus",
    "Acer",
    "Google",
    "Sony",
    "Microsoft",
]


def gen_devices(n: int) -> list[Device]:
    return [Device(name=get_random_device_name()) for _ in range(n)]


def get_random_device_name() -> str:
    return f"{brands[random.randint(0, len(brands) - 1)]}-{gen_random_str(2)}{random.randint(10, 100)}"


def gen_random_str(length: int) -> str:
    return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=length))
