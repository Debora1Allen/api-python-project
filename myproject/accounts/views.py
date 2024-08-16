from rest_framework import generics
from rest_framework.permissions import AllowAny
from accounts.models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse  


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


def home(request):  
    return HttpResponse("Bem-vindo ao meu projeto Django!")