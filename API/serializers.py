from SDPM_base.models import Item
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

User = get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # sustituye username por el email
        token['email'] = user.email
        return token
    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        # Verificamos que el email y la contraseña estén presentes
        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("No active account found with the given credentials")

            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password")

            # Está autenticando por email
            attrs["user"] = user  # Pasar el objeto usuario en lugar de 'username'
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return super().validate(attrs)