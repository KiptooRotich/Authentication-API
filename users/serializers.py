from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'location', 'profile_picture', 'is_active', 'is_staff'
        ]
        read_only_fields = ['id', 'email', 'is_active', 'is_staff']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
            return User.objects.create_user(**validated_data)
        
class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        
        if user:
            if not user.is_active:
                 raise serializers.ValidationError("Account is inactive.")
            
            if not user.is_email_verified:
                 raise serializers.ValidationError("Please verify your email before logging in.")
            
            return user
        else: 
            raise serializers.ValidationError("Invalid credentials")
    
class DeleteAccountSerializer(serializers.Serializer):
     password = serializers.CharField(write_only=True)

     def validate_password(self, value):
          password = serializers.CharField(write_only=True)

          def validate_password(self, value):
               user = self.content['request'].user
               if not user.check_password(value):
                    raise serializers.ValidationError("Incorrect password")
               return value