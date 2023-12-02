from django.http import JsonResponse
from django.shortcuts import redirect, render
from login.models import UserProfile
from django.contrib.auth.models import User
import json

# Create your views here.
def index(request):
    return JsonResponse({"Message":"Hello this is from profile app"})

def show_form_update_profile(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user__username=request.user)
        print(user.get_data())
        context = {
            "user": user.get_data()
        }
        return render(request, 'form_update_profile.html', context)
    else:
        return redirect('login:login_user')

def update_profile(request, username):
    if request.method == 'POST':
        data = json.loads(request.body)
        bio = data.get("bio")
        new_username = data.get("username")
        user_profile = UserProfile.objects.get(user__username=username)
        user_profile.bio = bio
        user_profile.save()
        try:
            user = User.objects.get(username=username)
            user.username = new_username
            user.save()
        except User.DoesNotExist:
            return JsonResponse({
                "Message": "User not found"
            })
        return JsonResponse({
            "redirect_url": f'/profile/{new_username}/'
        })
        return redirect('profile_user:get_profile_by_username', username=new_username)
    else:
        return redirect('profile_user:show_form_update_profile')

def get_profile_by_username(request, username):
    print(request.user)
    print(request.user.is_authenticated)
    user = UserProfile.objects.get(user__username=username)
    context = {
        "user": user.get_data()
    }
    return render(request, 'profile.html', context)