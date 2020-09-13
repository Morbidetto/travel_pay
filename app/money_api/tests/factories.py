import factory
from django.utils.timezone import get_current_timezone
from money_api.enums import BalanceChangeType
from money_api.models import Account
from money_api.models import AccountHistory


class AccountFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    balance = factory.Faker("pyint")

    class Meta:
        model = Account


class AccountHistoryFactory(factory.django.DjangoModelFactory):
    account = factory.SubFactory(AccountFactory)
    date = factory.Faker("date_time", tzinfo=get_current_timezone())
    reason = factory.Faker("random_element", elements=[el[0] for el in BalanceChangeType.choices])
    amount = factory.Faker("pyint", min_value=-500, max_value=500)

    class Meta:
        model = AccountHistory
