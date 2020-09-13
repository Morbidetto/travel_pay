from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from money_api.models import Account
from money_api.models import AccountHistory
from money_api.schemas import change_balance_post
from money_api.serializers import AccountHistorySerializer
from money_api.serializers import AccountSerializer
from money_api.serializers import ChangeBalanceSerializer


class AccountViewSet(ReadOnlyModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = (
        "first_name",
        "last_name",
        "email",
    )
    ordering_fields = ("firt_name", "last_name", "email", "id", "balance")
    filterset_fields = ("email", "balance", "first_name", "last_name")


class AccountHistoryViewSet(ReadOnlyModelViewSet):
    serializer_class = AccountHistorySerializer
    queryset = AccountHistory.objects.select_related("account").all()
    filter_backends = (
        filters.DjangoFilterBackend,
        OrderingFilter,
    )
    ordering_fields = (
        "date",
        "amount",
        "account",
    )
    filterset_fields = ("date", "account")


@method_decorator(name="post", decorator=swagger_auto_schema(**change_balance_post))
class ChangeBalanceView(APIView):
    def post(self, request):
        serializer = ChangeBalanceSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            try:
                response = serializer.save()
            except ValueError as exc:
                return Response({"message": repr(exc)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(response, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
