from django.urls import path
from . import views

# router = SimpleRouter()
# router.register('profile/', views.ProfileDetail.as_view(), basename='profile')


urlpatterns = [
    path('register', views.register, name='register'),
    path('personaldetail', views.personalDetails, name='personaldetail'),
    path('nextofkin', views.nextofKin, name='nextofkin'),
    path('healthinfo', views.healthInfo, name='healthinfo'),
    path('', views.loginPage, name='login'),
    path('profile', views.profile, name='profile'),
    path('face', views.face, name='face'),
    path('finger', views.finger, name='finger'),
    # path('', views.loginPage, name='login'),
    path('logout', views.logoutuser, name='logout'),

]
