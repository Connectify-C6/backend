from django.http import JsonResponse
from django.shortcuts import redirect, render
from login.models import UserProfile
from django.contrib.auth.models import User
from report.models import Report
import json
from django.shortcuts import get_object_or_404
# Create your views here.
def index(request):
    return JsonResponse({"Message":"Hello this is from profile app"})

def show_form_update_profile(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user__username=request.user)
        print(user.get_data())
        context = {
            "bio": user.bio,    
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
    # Fetch the requested user's profile
    print(request.user)
    
    if not request.user.is_authenticated:
        return redirect('login:login_user')
    
    user = get_object_or_404(UserProfile, user__username=username)

    print(user.get_data()['username'])
    # Fetch the logged-in user
    logged_in_user = request.user
    
    # Check if the logged-in user has already reported this profile
    already_reported = Report.objects.filter(reported_user=user.user, reporter=logged_in_user).exists()

    context = {
        "this_user": user.get_data(),
        "username": user.get_data()['username'],
        "role": user.role,
        "bio": user.bio,
        "already_reported": already_reported
    }

    print(user.get_data())

    return render(request, 'profile.html', context)