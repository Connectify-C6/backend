from django.shortcuts import render
# import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
import community
import login
from login.models import UserProfile
# import json
from rest_framework.parsers import JSONParser
import json
from invitation.models import *
from community.models import *
from community.views import join_community  
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            list_community_invitation = CommunityInvitation.objects.filter(receiver=request.user, is_responded=False)
            list_friend_request = FriendRequest.objects.filter(receiver=request.user)
            # list of dict of community invitation : id, sender, community, pesan
            list_community_invitation = list_community_invitation
            # list of dict of friend request : id, sender, pesan
            list_friend_request = list_friend_request
            context = {"Message":"My Invitations",
                             "user":request.user,
                             "list_community_invitation": list_community_invitation,
                            "list_friend_request": list_friend_request  
                            }
            print(context)
            return render(request, "show_invitation.html", context)
    else:
        return JsonResponse({"Message":"user belum login"}, status=401)


@csrf_exempt
def accept_community_invitation(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            # get data from request
            invitation_id = int(data.get("invitation_id"))
            print(type(invitation_id))
            invitation = CommunityInvitation.objects.get(id=invitation_id)
            invitation.is_responded = True
            invitation.save()
            
            community = invitation.community
            community.jumlah_anggota += 1
            community.save()
            print(community.jumlah_anggota, community.nama_community)
            # create anggota
            anggota = Anggota.objects.create(
                community=community,
                user=request.user
            )
            anggota.save()


            invitation.delete()
            print(invitation)
            return JsonResponse({"Message":"Invitation accepted",
                                 "success": True}, status=200)
        else:
            return JsonResponse({"Message":"Method not allowed",
                                 "success": False}, status=405)
    else:
        return JsonResponse({"Message":"user belum login",
                             "success": False}, status=401)
    
@csrf_exempt
def decline_community_invitation(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            # get data from request
            print(type(data.get("invitation_id")))
            invitation_id = int(data.get("invitation_id"))
            invitation = CommunityInvitation.objects.get(id=invitation_id)
            invitation.is_responded = True
            invitation.save()

            invitation.delete()
            return JsonResponse({"Message": "Invitation declined",
                                 "success": True
                                 
                                 }, status=200)
        else:
            return JsonResponse({"Message": "Method not allowed",
                                 "success" : False}, status=405)
    else:
        return JsonResponse({"Message": "user belum login",
                             "success" : False
                             }, status=401)

@csrf_exempt
def accept_friend_request(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            # get data from request
            friend_request_id = data.get("friend_request_id")
            friend_request = FriendRequest.objects.get(id=friend_request_id)
            friend_request.is_responded = True
            friend_request.save()
            friend_request.delete()
            return JsonResponse({"Message": "Friend request accepted"}, status=200)
        else:
            return JsonResponse({"Message": "Method not allowed"}, status=405)
    else:
        return JsonResponse({"Message": "user belum login"}, status=401)

