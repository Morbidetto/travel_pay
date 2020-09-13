import csv
from collections import defaultdict

from django.conf import settings
from django.db import transaction
from django.db.models import F

from money_api.models import Account


class CSVImporter:
    headers = {"id", "first_name", "last_name", "email", "referrer_email", "balance"}

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def read_and_save_data(self):
        instances, refferals = self.__parse_csv_file()
        with transaction.atomic():
            Account.objects.bulk_create([Account(**account) for account in instances])
            accounts = Account.objects
            for key, value in refferals.items():
                accounts.filter(email=key).update(balance=F("balance") + value)

    def __parse_csv_file(self):
        reader = csv.DictReader(self.csv_file, skipinitialspace=True)
        if not set(reader.fieldnames) == self.headers:
            raise ValueError("CSV headline contains not allowed headers")
        data = []
        refferals = defaultdict(lambda: 0)
        for row in reader:
            if row["referrer_email"]:
                refferals[row["referrer_email"]] += settings.RECOMMENDATION_IMPORT_BONUS
            row.pop("referrer_email")
            data.append(row)
        return data, refferals
