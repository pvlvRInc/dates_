from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken import views
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from date.models import User
from date.user.serializer import UserRegisterSerializer


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


@csrf_exempt
@api_view(["GET"])
def test_api(request):
    data = {'response': 'login successfully'}
    return Response(data, status=status.HTTP_200_OK)
