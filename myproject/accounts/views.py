from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            untapped_token = UntypedToken(token)
            user = User.objects.get(id=untapped_token['user_id'])
            
            if not user.is_active:
                user.is_active = True
                user.save()
                return HttpResponse("Email verified successfully!", status=200)
            else:
                return HttpResponse("Email is already verified.", status=200)
        except (User.DoesNotExist, InvalidToken):
            return HttpResponse("Invalid or expired token.", status=400)


def home(request):  
    return HttpResponse("Bem-vindo!")
