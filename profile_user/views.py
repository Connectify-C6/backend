from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from login.models import UserProfile
import json

# Create your views here.
def index(request):
    return JsonResponse({"Message":"Hello this is from profile app"})


@csrf_exempt
def update_profile(request, username):
    if request.method == 'POST':
        data = json.loads(request.body)
        bio = data.get("bio")
        new_username = data.get("username")
        user = UserProfile.objects.get(user__username=username)
        user.bio = bio
        user.username = new_username
        user.save()
        return JsonResponse({
            "user": user.get_data()
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