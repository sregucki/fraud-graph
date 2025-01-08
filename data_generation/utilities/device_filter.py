from data_generation.model.account import Account
from data_generation.model.device import Device


def filter_unused_devices(
    devices: list[Device], accounts: list[Account]
) -> list[Device]:
    used_devices_ids = set([account.device.id for account in accounts])
    return [device for device in devices if device.id in used_devices_ids]
