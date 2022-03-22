from django.urls import path
from date.views import user_register

urlpatterns = [
    path('clients/create', user_register, name='register'),
]