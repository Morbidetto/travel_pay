from django.db import models
from money_api.enums import BalanceChangeType


class Account(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    balance = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.email}"


class AccountHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.CharField(choices=BalanceChangeType.choices, max_length=128)
    amount = models.IntegerField()
