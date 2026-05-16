from django.urls import path

from .views import (
    PaymentFailedView,
    PaymentSuccessView,
    ProductsView,
    StartPaymentView,
    TransactionStatusView,
)

app_name = "payments"

urlpatterns = [
    path("products/", ProductsView.as_view(), name="products"),
    path("start/<str:product_code>/", StartPaymentView.as_view(), name="start"),
    path("status/<uuid:transaction_id>/", TransactionStatusView.as_view(), name="transaction_status"),
    path("success/", PaymentSuccessView.as_view(), name="success"),
    path("failed/", PaymentFailedView.as_view(), name="failed"),
]
