from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, CustomAuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    """Для регистрации новых пользоватетей."""
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User registered successfully!",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    """Для входа в аккаунт зарегестрированных пользователей."""
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        logger.info(type(request))
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user'] # type:ignore
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})