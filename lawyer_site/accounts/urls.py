from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('redact-profile/', views.redact_profile, name='redact_profile'),
    path('logout/', views.logout_user, name='logout'),
    path('deactivate/', views.deactivate_account, name='deactivate_account'),
    # Add other URL patterns for account-related views here
]