from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import Resetotp

# Normal User
class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_customer', 'is_staff','password','confirm_password']
        read_only_fields = ['is_staff', 'is_customer']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password and confirm password do not match"})
        return attrs

    # Custom create method to set password safely
    def create(self,validated_data):
        validated_data.pop('confirm_password')
        user=User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            is_customer=True,
            is_staff=False
        )
        password = validated_data.pop('password')
        if password:
            user.set_password(password)
            user.save()
            return user

# Admin User
class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_customer', 'is_staff','password','is_superuser']
        read_only_fields=['is_staff','is_customer','is_superuser']


    def validate(self,attrs):
    # Check if an admin already exists
        if User.objects.filter(is_staff=True, is_superuser=True).exists():
            raise serializers.ValidationError({"admin": "An admin already exists. You cannot create another one."})
        
        return attrs
    def create(self, validated_data):
        password = self.context['request'].data.get('password')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_customer=False,
            is_staff=True,
            is_superuser=True
        )
        if password:
            user.set_password(password)
            user.save()
        return user

customuser= get_user_model()

class Forgetpasswordserializer(serializers.Serializer):
    email=serializers.EmailField()

    def validate_email(self,value):
        if not customuser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No accounts with this email")
        return value
    
    def create(self,validated_data):
        email=validated_data['email']
        user=customuser.objects.get(email=email)

        otp=str(random.randint(100000,999999))
        Resetotp.objects.create(user=user,otp=otp)

        send_mail(
            "Your Password Reset OTP",
            f"Your OTP is {otp}. It will expire in 10 minutes.",
            "poppysayana@gmail.com",  # sender
            [email],
        )

        return {"message": "OTP sent to your email"}
        

class ResetPasswordserializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password":"passwords does not match"})
        
        email=attrs["email"]
        otp=attrs["otp"]

        try:
            user=customuser.objects.get(email=email)
        except customuser.DoesNotExist:
            raise serializers.ValidationError({"email":"invalid_email"})
        
        otp_record=Resetotp.objects.filter(user=user,otp=otp,is_used=False).last()

        if not otp_record:
            raise serializers.ValidationError({"invalid otp"})
        
        if now() - otp_record.created_at > timedelta(minutes=10):
            raise serializers.ValidationError({"otp": "OTP expired"})
        
        attrs["user"] = user
        attrs["otp_record"] = otp_record
        return attrs
    
    def create(self, validated_data):
        user=validated_data["user"]
        otp_record=validated_data['otp_record']

        user.set_password(validated_data["password"])
        user.save()

        otp_record.is_used=True
        otp_record.save()

        return {"message": "Password reset successful"}