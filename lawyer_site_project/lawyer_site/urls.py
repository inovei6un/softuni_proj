from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from .views import AppointmentView, IndexView, AboutView, PracticeView, ContactView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('practice/', PracticeView.as_view(), name='practice'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('appointment/', AppointmentView.as_view(), name='appointment'),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
]
