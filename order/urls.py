from django.urls import path
from .views import CreateOrderAPIView,VerifyPaymentAPIView,Addressview,DirectBuyAPIView

urlpatterns = [
    path("address/", Addressview.as_view(), name="address-list-create"),
    path("create/", CreateOrderAPIView.as_view(), name="create-order"),
    path("verify/", VerifyPaymentAPIView.as_view(), name="verify-payment"),
    path('direct-buy/', DirectBuyAPIView.as_view(), name='direct-buy'),
]
