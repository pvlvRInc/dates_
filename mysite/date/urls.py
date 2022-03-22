from django.urls import path
from date.views import RegisterUserView, test_api

urlpatterns = [
    path('clients/create', RegisterUserView.as_view(), name='register'),
    path('login_test', test_api),
]
