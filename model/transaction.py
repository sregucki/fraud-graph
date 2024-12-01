from datetime import datetime

from model.abc.entity import Entity
from model.account import Account


class Transaction(Entity):
    def __init__(
        self,
        source_account: Account,
        target_account: Account,
        amount: float,
        timestamp: datetime,
    ) -> None:
        super().__init__()
        self.source_account = source_account
        self.target_account = target_account
        self.amount = amount
        self.timestamp = timestamp

    def __str__(self) -> str:
        return f"{self.timestamp} | {self.source_account} -> {self.target_account} : {self.amount}"

    def __repr__(self) -> str:
        return self.__str__()