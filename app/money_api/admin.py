from django.contrib import admin

from money_api.models import Account
from money_api.models import AccountHistory


@admin.decorators.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "balance")
    list_editable = ("first_name", "last_name")


@admin.decorators.register(AccountHistory)
class AccountHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "reason", "amount", "account")
    list_editable = ()

    def has_add_permission(self, request):
        return False
