from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User
from reviews.validators import validate_username

MAX_LEN = 150
LEN_EMAIL = 254


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=LEN_EMAIL)
    username = serializers.SlugField(
        required=True,
        max_length=MAX_LEN,
        validators=[RegexValidator(r'^[\w.@+-]+$'), validate_username],
    )


class TokenSerializers(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=MAX_LEN,
        validators=[
            RegexValidator(r'^[\w.@+-]+$'),
            UniqueValidator(queryset=User.objects.all()),
        ],
    )
    email = serializers.EmailField(
        max_length=LEN_EMAIL,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
