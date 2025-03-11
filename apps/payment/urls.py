from django.urls import path
from .views import checkout, payment, process_payment, success, failure
urlpatterns = [
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment, name='payment'),
    path('process-payment/', process_payment, name='process_payment'),
    path('payment/success/', success, name='success'),
    path('payment/failure/', failure, name='failure'),
]
