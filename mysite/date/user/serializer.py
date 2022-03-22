from rest_framework import serializers

from date.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'gender', 'email', 'photo', 'password', 'password2')

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            photo=self.validated_data['photo'],
            gender=self.validated_data['gender'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password2 != password:
            raise serializers.ValidationError({'Не совпадают пароли': password})

        user.set_password(password2)

        user.save()

        return user