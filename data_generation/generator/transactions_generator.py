import random

from data_generation.generator.entity_generator import (
    gen_accounts,
    gen_accounts_in_country,
)
from data_generation.model.account import Account
from data_generation.model.transaction import Transaction
from data_generation.utilities.faker import faker


def __get_random_accounts_pair(accounts: list[Account]) -> tuple[Account, Account]:
    source_account_idx = random.randint(0, len(accounts) - 1)
    target_account_idx = random.randint(0, len(accounts) - 1)
    # Uniknięcie sytuacji, w której źródło i cel są takie same
    while target_account_idx == source_account_idx:
        target_account_idx = random.randint(0, len(accounts) - 1)
    return accounts[source_account_idx], accounts[target_account_idx]


def gen_normal_transactions(accounts: list[Account], n: int) -> list[Transaction]:
    return [
        Transaction(
            *__get_random_accounts_pair(accounts),
            round(
                random.uniform(0.01, 10000), 2
            ),  # losowa kwota z przedziału 0.01 - 10000
            faker.date_time_this_year(),
        )
        for _ in range(n)
    ]


def gen_circular_transactions(
    accounts: list[Account], n: int, min_cycle_length: int, max_cycle_length
) -> list[Transaction]:
    """
    :param accounts:
    :param n:
    :param min_cycle_length: minimalna ilość transakcji w pętli
    :param max_cycle_length: maksymalna ilość transakcji w pętli
    :return:
    """
    circular_transactions = []
    print(f"Generated {n} circular transactions: ")
    for _ in range(n):
        loop_size = random.randint(min_cycle_length, max_cycle_length)
        accounts_loop = random.sample(accounts, loop_size)
        loop = "["
        for i in range(loop_size):
            circular_transactions.append(
                Transaction(
                    accounts_loop[i],
                    accounts_loop[
                        (i + 1) % loop_size
                    ],  # modulo, aby ostatnie konto w pętli było połączone z pierwszym
                    round(random.uniform(0.01, 10000), 2),
                    faker.date_time_this_year(),
                )
            )
            loop += f"accountId={accounts_loop[i].id} ({accounts_loop[i].name}) -> "
        loop += f"accountId={accounts_loop[0].id} ({accounts_loop[0].name})]"
        print(f"Circular transaction: {loop}")
    return circular_transactions


def gen_transactions_with_communities(
    accounts: list[Account],
    n: int,
    community_max_size: int,
) -> list[Transaction]:
    """
    :param accounts:
    :param n:
    :param community_max_size: maksymalna ilość kont w społeczności (grupy transakcji pomiędzy kontami)
    :return:
    """
    print(f"Generated {n} communities: ")
    transactions = []
    for _ in range(n):
        community_accounts = random.sample(
            accounts,
            random.randint(
                3, community_max_size
            ),  # wybór losowych kont do społeczności
        )
        community_transactions = []
        for _ in range(2 * len(community_accounts)):
            community_transactions.append(
                Transaction(
                    *__get_random_accounts_pair(community_accounts),
                    round(random.uniform(0.01, 10000), 2),
                    faker.date_time_this_year(),
                )
            )
        print(
            f"Community: Number of transactions within community={len(community_transactions)}, Accounts={[f"accountId={account.id} ({account.name})" for account in community_accounts]}"
        )
        transactions += community_transactions
    return transactions


def gen_multi_transactions_to_acc_outside_country(
    n: int,
) -> tuple[list[Account], list[Transaction]]:
    transactions = []
    accounts = []
    print(f"Generated {n} multi-transactions to single accounts outside the country: ")
    for _ in range(n):
        target_account = gen_accounts(1)[0]  # mogą się wygenerować te same kraje
        source_accounts = gen_accounts_in_country(random.randint(3, 8), faker.country())
        print(
            f"Multi-transaction to accountId={target_account.id} ({target_account.location.country}) ({target_account.name}) from accounts located in ({source_accounts[0].location.country}) : {[f'accountId={account.id} ({account.name})' for account in source_accounts]}"
        )
        for source_account in source_accounts:
            transactions.append(
                Transaction(
                    source_account,
                    target_account,
                    round(random.uniform(0.01, 10000), 2),
                    faker.date_time_this_year(),
                )
            )
        accounts += source_accounts
        accounts.append(target_account)
    return accounts, transactions
