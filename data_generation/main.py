from data_generation.assigner.device_assigner import (
    assign_single_device_to_multiple_accounts,
)
from data_generation.generator.transactions_generator import (
    gen_normal_transactions,
    gen_circular_transactions,
    gen_transactions_with_communities,
)
from data_generation.utilities.entity_csv_writer import write_to_csv
from generator.entity_generator import gen_accounts, gen_devices


NUM_ACCOUNTS = 200
NUM_DEVICES = 200
NUM_TRANSACTIONS = 2000  # liczba "normalnych" transakcji
NUM_CIRCULAR_TRANSACTIONS = (
    30  # liczba transakcji "cyklicznych" (w pętlach) np. konto A -> B -> C -> A
)
NUM_DEVICES_WITH_MULTIPLE_ACCOUNTS = 10
MAX_DEVICES_PER_ACCOUNT = 5
COMMUNITIES_MAX_SIZE = 10
NUM_OF_COMMUNITIES = 10


def main():
    # generowanie kont i urządzeń
    accounts = gen_accounts(NUM_ACCOUNTS)
    devices = gen_devices(NUM_DEVICES)

    # generowanie "normalnych" transakcji
    transactions = gen_normal_transactions(accounts=accounts, quantity=NUM_TRANSACTIONS)

    # dodawanie transakcji w pętlach (circular transactions) | początek i koniec pętli to samo konto, pozostałe to najczęściej słupy
    transactions += gen_circular_transactions(
        accounts=accounts,
        quantity=NUM_CIRCULAR_TRANSACTIONS,
        min_cycle_length=3,
        max_cycle_length=8,
    )

    print("\n")
    # przypisywanie tych samych urządzeń do wielu kont
    assign_single_device_to_multiple_accounts(
        accounts, devices, NUM_DEVICES_WITH_MULTIPLE_ACCOUNTS, MAX_DEVICES_PER_ACCOUNT
    )

    print("\n")
    # stworzenie clusterów kont (communities detection)
    transactions += gen_transactions_with_communities(
        accounts, NUM_OF_COMMUNITIES, COMMUNITIES_MAX_SIZE
    )

    write_to_csv(accounts, "accounts.csv")
    write_to_csv(
        devices, "devices.csv"
    )  # to ma sens o ile będziemy chcieli stworzyć generator nazw urządzeń etc. - dodatkowe pola dla Device
    write_to_csv(transactions, "transactions.csv")


if __name__ == "__main__":
    main()
