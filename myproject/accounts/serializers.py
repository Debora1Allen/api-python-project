from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # User is inactive until they confirm their email
        )

        # Generate a token for email confirmation
        token = RefreshToken.for_user(user).access_token

        # Build email verification link using the Django backend URL
        verification_link = f"{settings.BACKEND_URL}{reverse('verify-email')}?token={token}"

        # Send email
        send_mail(
            'Email Verification',
            f'Please verify your email by clicking on the following link: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        
        if not user.is_active:
            raise serializers.ValidationError("Email not verified. Please verify your email.")

        data = super().validate(attrs)
        data['user'] = {
            "email": user.email,
            "username": user.username,
        }
        return data

