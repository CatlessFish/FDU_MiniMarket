from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginViewClass.as_view(), name='login'),
    path('register/', views.RegisterViewClass.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
]