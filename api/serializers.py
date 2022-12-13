from rest_framework import serializers
from django.contrib.auth import authenticate,login,logout
from accounts.models import *
from questions.models import *
import datetime,jwt
import re
from datetime import timedelta
from django.db.models import Max, Min, Count, Avg,Sum
from django.contrib.auth.hashers import make_password
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password','name')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name']
    
class VerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verifyemail
        fields=('id', 'email', 'code')
        extra_kwargs = {'code': {'write_only': True}}


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=['id','choice','question']