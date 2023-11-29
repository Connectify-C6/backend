from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer, UserProfileSerealizer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
import json
from django.contrib.auth import get_user_model
# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    return JsonResponse({"Message":"Hello World"})

@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        # cek jika username sudah ada
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None:
            return JsonResponse({"message": "Username already exist"}, status=400)
        else:
            user = User.objects.create_user(username=username, password=password)

            user_profile_serializer = UserProfileSerealizer(data={
                "role": "common_user",
                "bio": "",
                "count_reported": 0,
                "user": user.id
            })

            if user_profile_serializer.is_valid():
                user_profile_serializer.save()
                return JsonResponse({"message": "data :" + str(user_profile_serializer.data)}, status=200)
            else:
                return JsonResponse({"message": user_profile_serializer.errors}, status=400)
    else:
        return render(request, "register.html")
    

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        print(username)
        print(password)

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"message": "Username does not exist"}, status=400)

        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            if user.is_active:
                login(request, user)
                user_profile = UserProfile.objects.get(user=user)
                return JsonResponse({"message":"Login is successfully", "user_data":{
                    "username": user.username,
                    "role": user_profile.role,
                    "bio": user_profile.bio,
                    "count_reported": user_profile.count_reported
                }}, status=200)
            else:
                return JsonResponse({"message": "User is inactive"}, status=400)
        else:
            return JsonResponse({"message": "Incorrect password"}, status=400)
    else:
        return render(request, "login.html")

@csrf_exempt
def logout_user(request):
    logout(request) 
    return redirect("login:login_user")