from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from money_api.views import AccountHistoryViewSet
from money_api.views import AccountViewSet
from money_api.views import ChangeBalanceView

router = DefaultRouter()
router.register("accounts", AccountViewSet, basename="accounts")
router.register("history", AccountHistoryViewSet, basename="history")

schema_view = get_schema_view(
    openapi.Info(title="Money API", default_version="v1", description="API to list and modify accounts",), public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/change_balance", ChangeBalanceView.as_view(), name="change_balance"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
