from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.RegisterView, name='register'),
    path('', views.DashboardView, name='dashboard')
]