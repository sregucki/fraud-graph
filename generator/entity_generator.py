from faker import Faker

from model.account import Account
from model.device import Device

faker = Faker()


def gen_accounts(n: int) -> list[Account]:
    return [Account(faker.name(), faker.email()) for _ in range(n)]


def gen_devices(n: int) -> list[Device]:
    return [Device() for _ in range(n)]
