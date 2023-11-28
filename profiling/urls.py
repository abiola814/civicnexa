from django.urls import path
from django.views.generic import TemplateView
from . import views
from rest_framework.schemas import get_schema_view
# from rest_framework.routers import SimpleRouter

# router = SimpleRouter()
# router.register('profile/', views.ProfileDetail.as_view(), basename='profile')


urlpatterns = [
    path('profile/', views.ProfileDetail.as_view()),
    path('getprofile/<str:user__email>', views.GetProfileApi.as_view()),
    # path('transactions/', views.ListTransactions.as_view()),
    path('edit-bank/', views.EditBank.as_view()),
    path('edit-nextofkin/', views.EditNextofKin.as_view()),
    path('adminpanel/', views.AdminPanel.as_view()),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name='activate_account'),
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),

  
        # ...
        # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
        #   * `title` and `description` parameters are passed to `SchemaGenerator`.
        #   * Provide view name for use with `reverse()`.
    path('openapi', get_schema_view(
            title="Your Project",
            description="API for all things …",
            version="1.0.0"
        ), name='openapi-schema'),
        # ...
    
]