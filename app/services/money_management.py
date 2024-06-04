from abc import ABC, abstractmethod

from app.db.models.user import User


class MoneyManagement:

    @abstractmethod
    def manage_money(self, account: User, money: float):
        raise NotImplementedError


class CoreAndSatteliteMoneyManagement(MoneyManagement):
    def __init__(self, account: User, money: float):
        self.core_money = money * 0.6
        self.sattelite_money = money * 0.4
