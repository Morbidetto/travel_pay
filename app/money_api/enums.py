from djchoices import ChoiceItem
from djchoices import DjangoChoices


class BalanceChangeType(DjangoChoices):
    reservation_bonus = ChoiceItem("reservation_bonus")
    award = ChoiceItem("award")
    promotion = ChoiceItem("promotion")
    recommendation = ChoiceItem("recommendation")
    hotel_reservation = ChoiceItem("hotel_reservation")
