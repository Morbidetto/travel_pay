import pytest
from django.urls import reverse
from money_api.enums import BalanceChangeType
from money_api.models import Account
from money_api.models import AccountHistory
from money_api.tests.factories import AccountFactory
from money_api.tests.factories import AccountHistoryFactory
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestAccountEndpoints:
    @pytest.fixture(autouse=True)
    def init(self):
        self.api_client = APIClient()
        AccountFactory.create_batch(5)

    def test_accounts_from_db_listed_properly(self):
        response = self.api_client.get(reverse("accounts-list"))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == Account.objects.all().count()

    def test_not_found_if_wrong_id_provided(self):
        response = self.api_client.get(reverse("accounts-detail", kwargs={"pk": 404}))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAccountHistoryEndpoints:
    @pytest.fixture(autouse=True)
    def init(self):
        self.api_client = APIClient()
        AccountHistoryFactory.create_batch(5)

    def test_accounts_from_db_listed_properly(self):
        response = self.api_client.get(reverse("history-list"))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == AccountHistory.objects.all().count()

    def test_not_found_if_wrong_id_provided(self):
        response = self.api_client.get(reverse("history-detail", kwargs={"pk": 404}))

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestChangeBalance:
    @pytest.fixture(autouse=True)
    def init(self):
        self.api_client = APIClient()
        self.account = AccountFactory.create(balance=0)

    def test_add_positive_balance(self):
        response = self.api_client.post(
            reverse("change_balance"),
            {"amount": 200, "reason": BalanceChangeType.reservation_bonus, "account": self.account.id},
        )
        assert response.status_code == status.HTTP_200_OK
        self.account.refresh_from_db()
        assert self.account.balance == 200
        assert AccountHistory.objects.filter(account=self.account).exists()

    def test_add_negative_balance(self):
        self.account.balance = 300
        self.account.save()
        response = self.api_client.post(
            reverse("change_balance"),
            {"amount": -200, "reason": BalanceChangeType.reservation_bonus, "account": self.account.id},
        )
        assert response.status_code == status.HTTP_200_OK
        self.account.refresh_from_db()
        assert self.account.balance == 100
        assert AccountHistory.objects.filter(account=self.account).exists()

    def test_add_negative_balance_exception(self):
        response = self.api_client.post(
            reverse("change_balance"),
            {"amount": -200, "reason": BalanceChangeType.reservation_bonus, "account": self.account.id},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self.account.refresh_from_db()
        assert self.account.balance == 0
        assert not AccountHistory.objects.filter(account=self.account).exists()

    def test_add_balance_wrong_account(self):
        response = self.api_client.post(
            reverse("change_balance"), {"amount": 200, "reason": BalanceChangeType.reservation_bonus, "account": 404}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_add_balance_wrong_balance(self):
        response = self.api_client.post(
            reverse("change_balance"),
            {"amount": 200.03, "reason": BalanceChangeType.reservation_bonus, "account": self.account.id},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
