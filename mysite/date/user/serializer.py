from rest_framework import serializers

from date.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    photo = serializers.ImageField(required=True)
    password2 = serializers.CharField()
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'gender', 'email', 'photo', 'latitude', 'longitude', 'password', 'password2')

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            photo=self.validated_data['photo'],
            gender=self.validated_data['gender'],
            latitude=self.validated_data['latitude'],
            longitude=self.validated_data['longitude'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password2 != password:
            raise serializers.ValidationError({'Не совпадают пароли': password})

        user.set_password(password2)

        user.save()

        return user


class UserMatchSerializer(serializers.ModelSerializer):
    MATCH_CHOICES = (
        ('L', 'Like'),
        ('D', 'Dislike'),
    )
    check = serializers.ChoiceField(choices=MATCH_CHOICES)

    class Meta:
        model = User
        fields = ('check',)

    def update(self, instance, validated_data, auth_user=None):
        auth_user.matches.add(instance)


class UserFilterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'latitude', 'longitude')
