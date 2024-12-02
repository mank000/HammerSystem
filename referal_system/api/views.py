from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from phone_numbers.models import HammerSystemUser

from .serializers import (NewCodeSerializer, ProfileSerializer,
                          RegistrationSerializer, VerificationSerializer)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer


class NewCodeView(generics.GenericAPIView):
    serializer_class = NewCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Код отправлен!"},
                        status=status.HTTP_200_OK)


class VerifyPhoneView(generics.GenericAPIView):
    serializer_class = VerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(
            {"detail": "Телефон успешно подтвержден!", "tokens": tokens},
            status=status.HTTP_200_OK
        )


class MyProfileView(generics.RetrieveUpdateAPIView):
    queryset = HammerSystemUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return HammerSystemUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user
