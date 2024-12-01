import random

from faker import Faker

from generator.entity_generator import gen_accounts, gen_devices
from model.transaction import Transaction
from utilities.entity_csv_writer import write_to_csv

faker = Faker()


def main():
    NUM_ACCOUNTS = 200  # liczba kont
    NUM_DEVICES = 200  # liczba urządzeń
    NUM_TRANSACTIONS = 2000  # liczba transakcji

    accounts = gen_accounts(NUM_ACCOUNTS)
    devices = gen_devices(NUM_DEVICES)

    # generowanie normalnych transakcji
    transactions = []
    for _ in range(NUM_TRANSACTIONS):
        source_account = random.randint(0, NUM_ACCOUNTS - 1)  # wybór losowych kont
        target_account = random.randint(0, NUM_ACCOUNTS - 1)
        # Uniknięcie sytuacji, w której źródło i cel są takie same
        while target_account == source_account:
            target_account = random.randint(0, NUM_ACCOUNTS - 1)
        transactions.append(
            Transaction(
                accounts[source_account],
                accounts[target_account],
                round(random.uniform(0.01, 10000), 2),
                faker.date_time_this_year(),
            )
        )

    # print_in_lines(transactions)

    # dodawanie transakcji w pętlach (circular transactions) | początek i koniec pętli to samo konto, pozostałe to najczęściej słupy
    NUM_CIRCULAR_TRANSACTIONS = 30
    circular_transactions = []
    for _ in range(NUM_CIRCULAR_TRANSACTIONS):
        loop_size = random.randint(3, 7)  # liczba transakcji w pętli
        accounts_loop = random.sample(accounts, loop_size)  # wybór losowej próbki kont
        for i in range(loop_size):
            circular_transactions.append(
                Transaction(
                    accounts_loop[i],
                    accounts_loop[
                        (i + 1) % loop_size
                    ],  #  modulo, aby ostatnie konto w pętli było połączone z pierwszym
                    round(random.uniform(0.01, 10000), 2),
                    faker.date_time_this_year(),
                )
            )

    transactions += circular_transactions

    # przypisanie urządzeń
    for i in range(len(accounts)):
        accounts[i].device = devices[i]

    # przypisywanie tych samych urządzeń do wielu kont
    NUM_DEVICES_WITH_MULTIPLE_ACCOUNTS = 10
    MAX_DEVICES_PER_ACCOUNT = 5
    devices_with_multiple_accounts = random.sample(
        devices, NUM_DEVICES_WITH_MULTIPLE_ACCOUNTS
    )
    for device in devices_with_multiple_accounts:
        accounts_with_device = random.sample(
            accounts, random.randint(1, MAX_DEVICES_PER_ACCOUNT)
        )
        for account in accounts_with_device:
            account.device = device
        print(f"{device} assigned to accounts: {accounts_with_device}")

    print("\n")

    # stworzenie clusterów kont (communities detection)
    COMMUNITIES_MAX_SIZE = 10
    NUM_OF_COMMUNITIES = 10
    for _ in range(NUM_OF_COMMUNITIES):
        community_size = random.randint(2, COMMUNITIES_MAX_SIZE)
        community_accounts = random.sample(accounts, community_size)
        for _ in range(2 * len(community_accounts)):
            source_account = random.choice(community_accounts)
            target_account = random.choice(community_accounts)
            while target_account == source_account:
                target_account = random.choice(community_accounts)
            transactions.append(
                Transaction(
                    source_account,
                    target_account,
                    round(random.uniform(0.01, 10000), 2),
                    faker.date_time_this_year(),
                )
            )

    write_to_csv(accounts, "accounts.csv")
    write_to_csv(
        devices, "devices.csv"
    )  # to ma sens o ile będziemy chcieli stworzyć generator nazw urządzeń etc. - dodatkowe pola dla Device
    write_to_csv(transactions, "transactions.csv")


if __name__ == "__main__":
    main()
