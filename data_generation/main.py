from data_generation.assigner.device_assigner import (
    assign_single_device_to_multiple_accounts,
)
from data_generation.generator.device_generator import gen_devices
from data_generation.generator.transactions_generator import (
    gen_normal_transactions,
    gen_circular_transactions,
    gen_transactions_with_communities,
    gen_multi_transactions_to_acc_outside_country,
)
from data_generation.log_collection.log_collector import clear_previous_logs
from data_generation.utilities.device_filter import filter_unused_devices
from data_generation.utilities.entity_csv_writer import write_to_csv
from generator.accounts_generator import gen_accounts


NUM_ACCOUNTS = 50
NUM_DEVICES = 50
NUM_TRANSACTIONS = 50  # liczba "normalnych" transakcji
NUM_CIRCULAR_TRANSACTIONS = (
    10  # liczba transakcji "cyklicznych" (w pętlach) np. konto A -> B -> C -> A
)
NUM_DEVICES_WITH_MULTIPLE_ACCOUNTS = 5
MAX_DEVICES_PER_ACCOUNT = 5
COMMUNITIES_MAX_SIZE = 7
NUM_OF_COMMUNITIES = 5
NUM_OF_MULTI_TRANSACTIONS_OUTSIDE_COUNTRY = 5


def main():
    clear_previous_logs()

    # generowanie kont i urządzeń
    accounts = gen_accounts(NUM_ACCOUNTS)
    devices = gen_devices(NUM_DEVICES)

    # generowanie "normalnych" transakcji
    transactions = gen_normal_transactions(accounts=accounts, n=NUM_TRANSACTIONS)

    # dodawanie transakcji w pętlach (circular transactions) | początek i koniec pętli to samo konto, pozostałe to najczęściej słupy
    transactions += gen_circular_transactions(
        accounts=accounts,
        n=NUM_CIRCULAR_TRANSACTIONS,
        min_cycle_length=3,
        max_cycle_length=8,
    )

    print("\n")
    multi_transactions_outside_country = gen_multi_transactions_to_acc_outside_country(
        NUM_OF_MULTI_TRANSACTIONS_OUTSIDE_COUNTRY
    )

    accounts += multi_transactions_outside_country[0]
    transactions += multi_transactions_outside_country[1]

    print("\n")
    # przypisywanie tych samych urządzeń do wielu kont
    devices += assign_single_device_to_multiple_accounts(
        accounts, devices, NUM_DEVICES_WITH_MULTIPLE_ACCOUNTS, MAX_DEVICES_PER_ACCOUNT
    )

    print("\n")
    # stworzenie clustrów kont (communities detection)
    transactions += gen_transactions_with_communities(
        accounts, NUM_OF_COMMUNITIES, COMMUNITIES_MAX_SIZE
    )

    devices = filter_unused_devices(devices=devices, accounts=accounts)

    write_to_csv(accounts, "accounts.csv")
    write_to_csv(
        devices, "devices.csv"
    )  # to ma sens o ile będziemy chcieli stworzyć generator nazw urządzeń etc. - dodatkowe pola dla Device
    write_to_csv(transactions, "transactions.csv")


if __name__ == "__main__":
    main()
