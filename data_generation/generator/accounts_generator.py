from model.account import Account

from data_generation.model.location import Location
from data_generation.utilities.faker import faker


def gen_accounts(n: int) -> list[Account]:
    return [
        Account(
            name=faker.name(),
            email=faker.email(),
            location=Location(faker.country(), faker.city(), faker.street_address()),
        )
        for _ in range(n)
    ]


def gen_accounts_in_country(n: int, country: str) -> list[Account]:
    return [
        Account(
            name=faker.name(),
            email=faker.email(),
            location=Location(country, faker.city(), faker.street_address()),
        )
        for _ in range(n)
    ]
