from django.shortcuts import render
# import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from login.models import UserProfile
# import json
from rest_framework.parsers import JSONParser
import json
from invitation.models import *
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            list_community_invitation = list(CommunityInvitation.objects.filter(receiver=request.user).values_list('community__nama_community', flat=True))
            list_friend_request = list(FriendRequest.objects.filter(receiver=request.user).values_list('sender__username', flat=True))
            return JsonResponse({"Message":"My Invitations",
                             "User":request.user.username,
                             "list_community_invitation": list_community_invitation,
                            "list_friend_request": list_friend_request
                                
                             }, status=200)
    else:
        return JsonResponse({"Message":"user belum login"}, status=401)

