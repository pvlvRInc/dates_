from django.urls import path
from rest_framework.authtoken import views

from date.views import RegisterUserView, MatchView, UserListView

urlpatterns = [
    path('clients/create', RegisterUserView.as_view(), name='register'),
    path('clients/<int:user_id>/match', MatchView.as_view(), name='match'),
    path('list', UserListView.as_view(), name='list'),
    path('obtain_token', views.obtain_auth_token)
]
