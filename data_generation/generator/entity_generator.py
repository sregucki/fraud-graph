from model.account import Account
from model.device import Device

from data_generation.utilities.faker import faker


def gen_accounts(n: int) -> list[Account]:
    return [Account(name=faker.name(), email=faker.email()) for _ in range(n)]


def gen_devices(n: int) -> list[Device]:
    return [Device() for _ in range(n)]
