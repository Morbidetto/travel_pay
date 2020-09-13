from datetime import datetime

from django.db import transaction
from django.utils.timezone import get_current_timezone
from money_api.enums import BalanceChangeType
from money_api.models import Account
from money_api.models import AccountHistory
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class AccountHistorySerializer(serializers.ModelSerializer):
    account_email = serializers.CharField(source="account.email")

    class Meta:
        model = AccountHistory
        fields = "__all__"


class ChangeBalanceSerializer(serializers.Serializer):
    date = serializers.HiddenField(default=datetime.now(tz=get_current_timezone()))
    amount = serializers.IntegerField()
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    reason = serializers.ChoiceField(choices=BalanceChangeType.choices)

    @transaction.atomic
    def create(self, validated_data):
        account = validated_data.pop("account")
        amount = validated_data.pop("amount")
        account = Account.objects.select_for_update().get(id=account.id)
        if account.balance + amount < 0:
            raise ValueError("Balance would be negative after this transaction")
        account.balance += amount
        account.save()
        AccountHistory.objects.create(
            account=account, amount=amount, date=validated_data["date"], reason=validated_data["reason"]
        )
        return {"message": f"Balance succesfuly updated, new balance is {account.balance}"}


class ChangeBalanceSerializerResponse(serializers.Serializer):
    message = serializers.CharField()
