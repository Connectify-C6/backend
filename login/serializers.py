from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password']

class UserProfileSerealizer(serializers.ModelSerializer):
    class Meta(object):
        model = UserProfile
        fields = ['user','role', 'bio', 'count_reported','user_id']