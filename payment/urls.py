from django.urls import path
from . import views

app_name='payments'


urlpatterns = [
    path('initiate/<str:fee>', views.initiate_payment, name="initiate-payment"),
    path('verify/<str:ref>/', views.verify_payment, name="verify-payment"),
    path('requestlogin/<str:state_code>', views.requestLogin, name='request'),
    path('payment', views.payment, name='payment'),
]