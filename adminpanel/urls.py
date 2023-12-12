from django.urls import path
from . import views

# router = SimpleRouter()
# router.register('profile/', views.ProfileDetail.as_view(), basename='profile')


urlpatterns = [
    # path('transaction', views.getTransaction, name='transactions'),
    path('profile', views.profile, name='adminprofile'),
    path('adminpanel', views.getProfile, name='adminpanel'),
    # path('alltransactions', views.getTransactionsApi),
    # path('usertransaction', views.userTransaction),
    path('', views.loginPage, name='govlogin'),
    path('logout', views.logoutuser, name='govlogout'),

]
