import django_filters
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from date.filters import UserFilter
from date.models import User
from date.user.serializer import UserRegisterSerializer, UserMatchSerializer, UserFilterListSerializer


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            data['username'] = serializer.validated_data['username']
            data['email'] = serializer.validated_data['email']

            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class MatchView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserMatchSerializer
    queryset = User.objects.all()

    def patch(self, request, *args, **kwargs):
        serializer = UserMatchSerializer(data=request.data)

        target_user_id = kwargs.pop('user_id')
        target_user = get_object_or_404(User, pk=target_user_id)

        auth_user = User.objects.get(username=request.user)

        data = {}
        if target_user == auth_user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            if serializer.validated_data['check'] == 'L':
                serializer.update(target_user, serializer.validated_data, auth_user=request.user)
                data['response'] = 'U liked person'
                if auth_user in target_user.matches.all():
                    mail = send_mail(
                        'Новая симпатия',
                        'У вас взаимная симпатия!',
                        'qwertygdd123@rambler.ru',
                        [target_user.email, auth_user.email],
                        fail_silently=False,
                    )
                    if mail:
                        data['mail'] = 'Check mail'
            else:
                data['response'] = 'U skipped person'

            return Response(data, status=status.HTTP_200_OK)

        else:
            data = serializer.errors
            return Response(data)


class UserListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    serializer_class = UserFilterListSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = User.objects.all().exclude(is_superuser=True)
    filterset_class = UserFilter

