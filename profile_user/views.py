from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from login.models import UserProfile
from django.core import serializers

# Create your views here.
def index(request):
    return JsonResponse({"Message":"Hello this is from profile app"})

def show_profile_by_username(request, username):
    user = UserProfile.objects.get(user__username=username)
    print(user.get_data())
    return JsonResponse({
        "user": user.get_data()
    })

def update_profile(request, username):
    if request.method == 'POST':
        user = UserProfile.objects.get(user__username=username)
        user.bio = request.POST['bio']
        user.save()
        return JsonResponse({
            "user": user.get_data()
        })
    else:
        return JsonResponse({
            "Message": "Failed to update profile"
        })