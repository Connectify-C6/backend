from django.http import JsonResponse
from login.models import UserProfile
from django.contrib.auth.models import User
import json

# Create your views here.
def index(request):
    return JsonResponse({"Message":"Hello this is from profile app"})

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
            "user": user_profile.get_data()
        })
    else:
        return JsonResponse({
            "Message": "Failed to update profile"
        })

def get_profile_by_username(request, username):
    user = UserProfile.objects.get(user__username=username)
    print(user.get_data())
    return JsonResponse({
        "user": user.get_data()
    })