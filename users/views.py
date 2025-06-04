from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DeleteAccountSerializer, RegisterSerializer, LoginSerializers, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from users.models import User
from django.shortcuts import get_object_or_404
from .utils import send_password_reset_email, password_reset_token
from django.contrib.auth import authenticate

def send_verification_email(user, request):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_url = request.build_absolute_uri(
            reverse('verify-email') + f'?uid={uid}&token={token}'
        )

        subject = 'Verify your email address'
        message = f'Hi {user.email},\n\nPlease click the link below to verify your email:\n{verify_url}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

class RegisterView(generics.CreateAPIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request) # Send verification email
            return Response(
                {'messge': 'Registration successful. Check your email to verify your account'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request):
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_email_verified = True
                user.save()
                return Response({'message': 'Email verified successfully!'})
            else:
                return Response({'error': 'Invalid or expired token'},status=400)
            
        except Exception as e:
            return Response({'error': 'Invalid link'}, status=400)

class RequestPasswordResetView(APIView):
    def post(self, request):
        email =  request.data.get('email')
        user = get_object_or_404(User, email=email)
        send_password_reset_email(user, request)
        return Response({'message': 'Password rest link sent.'}, status=status.HTTP_200_OK)
    
class PasswodResetConfirmView(APIView):
    def post(self, request, uid, token):
        password = request.data.get('password')
        user= get_object_or_404(User, pk=uid)

        if password_reset_token.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            user =  serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    permisson_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        return Response({"details": "Successfully logged out."}, status=status.HTTP_200_OK)
    
class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "Account deactivated successfully"}, status=status.HTTP_200_OK)

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = DeleteAccountSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.delete()
            return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReactivateAccountView(APIView):
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            if user.is_active:
                return Response({"detail": "Account is already active."}, status=status.HTTP_400_BAD_REQUEST)
            
            user.is_active = True
            user.save()
            send_mail(
                "Accout Reactivated",
                "Your account has been successfully reactivated.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            return Response({"detail": "Account has been successfully reactivated."}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials or account does not exist."}, status=status.HTTP_400_BAD_REQUEST)