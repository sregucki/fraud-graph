import random

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


def gen_normal_transactions(
    accounts: list[Account], quantity: int
) -> list[Transaction]:
    return [
        Transaction(
            *__get_random_accounts_pair(accounts),
            round(
                random.uniform(0.01, 10000), 2
            ),  # losowa kwota z przedziału 0.01 - 10000
            faker.date_time_this_year(),
        )
        for _ in range(quantity)
    ]


def gen_circular_transactions(
    accounts: list[Account], quantity: int, min_cycle_length: int, max_cycle_length
) -> list[Transaction]:
    """
    :param accounts:
    :param quantity:
    :param min_cycle_length: minimalna ilość transakcji w pętli
    :param max_cycle_length: maksymalna ilość transakcji w pętli
    :return:
    """
    circular_transactions = []
    print(f"Generated {quantity} circular transactions: ")
    for _ in range(quantity):
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
    quantity: int,
    community_max_size: int,
) -> list[Transaction]:
    """
    :param accounts:
    :param quantity:
    :param community_max_size: maksymalna ilość kont w społeczności (grupy transakcji pomiędzy kontami)
    :return:
    """
    print(f"Generated {quantity} communities: ")
    transactions = []
    for _ in range(quantity):
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
