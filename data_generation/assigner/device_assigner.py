import random

from data_generation.generator.entity_generator import gen_devices
from data_generation.log_collection.log_collector import collect_log
from data_generation.model.account import Account
from data_generation.model.device import Device


def assign_single_device_to_multiple_accounts(
    accounts: list[Account],
    devices: list[Device],
    num_devices_with_multiple_accounts: int,
    max_devices_per_account: int,
) -> list[Device]:
    """
    :param accounts:
    :param devices:
    :param num_devices_with_multiple_accounts: liczba urządzeń, które zostaną przypisane do wielu kont
    :param max_devices_per_account: maksymalna liczba kont, do których zostanie przypisane jedno urządzenie
    :return:
    """
    if len(accounts) > len(devices):
        devices += gen_devices(len(accounts) - len(devices))
    collect_log("\nAssigning single devices to multiple accounts:")
    for i in range(
        len(accounts)
    ):  # przypisanie pojedynczego urządzenia do jednego konta
        accounts[i].device = devices[i]
    # wybranie losowych urządzeń, które zostaną przypisane do wielu kont
    devices_with_multiple_accounts = random.sample(
        devices, num_devices_with_multiple_accounts
    )
    for device in devices_with_multiple_accounts:
        # wybranie losowych kont, do których zostanie przypisane to samo urządzenie
        accounts_with_device = random.sample(
            accounts, random.randint(2, max_devices_per_account)
        )
        collect_log(
            f"Device {device} assigned to accounts: {[f"accountId:{account.id} ({account.name})" for account in accounts_with_device]}"
        )
        for account in accounts_with_device:
            account.device = device
    return devices_with_multiple_accounts
