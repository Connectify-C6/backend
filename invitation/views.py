from django.shortcuts import render
# import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from login.models import UserProfile
# import json
from rest_framework.parsers import JSONParser
import json
from invitation.models import *
from community.views import *
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            list_community_invitation = CommunityInvitation.objects.filter(receiver=request.user, is_responded=False)
            list_friend_request = FriendRequest.objects.filter(receiver=request.user)
            # list of dict of community invitation : id, sender, community, pesan
            list_community_invitation = list(list_community_invitation.values())
            # list of dict of friend request : id, sender, pesan
            list_friend_request = list(list_friend_request.values())
            return JsonResponse({"Message":"My Invitations",
                             "User":request.user.username,
                             "list_community_invitation": list_community_invitation,
                            "list_friend_request": list_friend_request
                                
                             }, status=200)
    else:
        return JsonResponse({"Message":"user belum login"}, status=401)


@csrf_exempt
def accept_community_invitation(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            # get data from request
            invitation_id = data.get("invitation_id")
            invitation = CommunityInvitation.objects.get(id=invitation_id)
            invitation.is_responded = True
            invitation.save()
            return join_community(request)
        else:
            return JsonResponse({"Message":"Method not allowed"}, status=405)
    else:
        return JsonResponse({"Message":"user belum login"}, status=401)
    
@csrf_exempt
def decline_community_invitation(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            # get data from request
            invitation_id = data.get("invitation_id")
            invitation = CommunityInvitation.objects.get(id=invitation_id)
            invitation.is_responded = True
            invitation.save()
            return JsonResponse({"Message":"Invitation declined"}, status=200)
        else:
            return JsonResponse({"Message":"Method not allowed"}, status=405)
    else:
        return JsonResponse({"Message":"user belum login"}, status=401)