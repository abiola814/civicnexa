from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# router = SimpleRouter()
# router.register('profile/', views.ProfileDetail.as_view(), basename='profile')


urlpatterns = [
    path('register', views.register, name='register'),
    path('personaldetail', views.personalDetails, name='personaldetail'),
    path('nextofkin', views.nextofKin, name='nextofkin'),
    path('healthinfo', views.healthInfo, name='healthinfo'),
    path('', views.loginPage, name='login'),
    path('profile', views.profile, name='profile'),
    # path('', views.loginPage, name='login'),
    path('logout', views.logoutuser, name='logout'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
