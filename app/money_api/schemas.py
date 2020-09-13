from money_api.serializers import ChangeBalanceSerializer
from money_api.serializers import ChangeBalanceSerializerResponse

change_balance_post = dict(
    operation_description="Change user balance.",
    responses={"200": ChangeBalanceSerializerResponse, "400": ChangeBalanceSerializerResponse},
    request_body=ChangeBalanceSerializer,
)
