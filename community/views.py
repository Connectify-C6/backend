from calendar import calendar
from operator import inv
from django.shortcuts import render
# import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Community, Anggota
from invitation.models import CommunityInvitation, FriendRequest, Invitation
from login.models import UserProfile
from django.contrib.auth.models import User
from django.core import serializers
from rest_framework.parsers import JSONParser
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/auth/login/')
def search(request):
    # check if user is authenticated
    if request.user.is_authenticated:
        # if method is post
        list_community = Community.objects.all()
        list_community_json = serializers.serialize('json', list_community)
        context = {
        "list_community": list_community_json,
        "user": request.user
        }
        return render(request, 'community.html', context)
                         
    else:
        return JsonResponse({"Message":"user belum login"}, status=400)

@login_required(login_url='/auth/login/')
def index(request):
    if request.user.is_authenticated:
        user_communities = Anggota.objects.filter(user=request.user)

        context = {
            'user_communities': user_communities,
            'user': request.user,
            
        }
        return render(request, 'my_community.html', context)
    else:
        return JsonResponse({"Message": "user belum login"}, status=401)
    

    

@csrf_exempt
def create_community(request):
    # check if user is authenticated
    print(request.user.is_authenticated)
    if request.user.is_authenticated:
       # if method is post
        if request.method == "POST":
            data = json.loads(request.body)
            # get data from request
            nama_community = data.get("namaCommunity")
            detail_community = data.get("detail")
            # check if nama_community is already exist, if yes, cannot create community
            if Community.objects.filter(nama_community=nama_community).exists():
                print({"message": "Nama Community sudah ada"})
                return JsonResponse({"message": "Nama Community sudah ada"}, status=400)
            else:
                # create community
                community = Community.objects.create(
                    nama_community=nama_community,
                    detail_community=detail_community,
                    leader=request.user,
                    jumlah_anggota=1,
                )
                # create anggota
                anggota = Anggota.objects.create(
                    community=community,
                    user=request.user
                )
                print({"message": "Community berhasil dibuat",
                                     "nama_community": community.nama_community,
                                     "leader": community.leader.username,
                                     })
                return JsonResponse({"message": "Community berhasil dibuat",
                                     "nama_community": community.nama_community,
                                     "leader": community.leader.username,
                                     }, status=200)
        else:
            return render(request, "create_community.html")
    else:
        return JsonResponse({"message": "User belum login"}, status=400)      

@csrf_exempt   
def join_community(request):
    # check if user is authenticated
    if request.user.is_authenticated:
        # if method is post
        if request.method == "POST":
            data = json.loads(request.body)
            # get nama_community from request
            nama_community = data.get("nama_community")
            # get community
            community = Community.objects.get(nama_community=nama_community)
            # check if user is already in community
            if Anggota.objects.filter(community=community, user=request.user).exists():
                return JsonResponse({"message": "User sudah bergabung dalam community ini"}, status=400)
            else:
                # create anggota
                anggota = Anggota.objects.create(
                    community=community,
                    user=request.user
                )
                # update jumlah anggota
                community.jumlah_anggota += 1
                community.save()
                return JsonResponse({"message": "User berhasil bergabung dalam community ini"}, status=200)
        else:
            return JsonResponse({"message": "Method not allowed"}, status=400)
    else:
        return JsonResponse({"message": "User belum login"}, status=400)

@csrf_exempt
def get_community_member(request, community_id):
    # check if user is authenticated
    if request.user.is_authenticated:
        # get community based on id
        community = Community.objects.get(id=community_id)
        # get all anggota from community
        anggota = Anggota.objects.filter(community=community)
        # get all user from anggota
        user = UserProfile.objects.filter(user__in=anggota.values_list('user', flat=True))
        # return all user
        is_leader = community.leader == request.user
        context = {
            "user": request.user,
            "is_leader": is_leader,
            "community": community,
            "anggota": user
        }
        return render(request, 'community_member.html', context)
    else:
        return JsonResponse({"message": "User belum login"}, status=400)
    

@csrf_exempt
def send_invitation(request):
    # check if user is authenticated
    if request.user.is_authenticated:
        # if method is post
        if request.method == "POST":

            data = json.loads(request.body)
            # get nama_community from request
            nama_community = data.get("nama_community")
            print(nama_community)
            if Community.objects.filter(nama_community=nama_community).exists():
                community = Community.objects.filter(nama_community=nama_community)[0]
                print(community)
                if request.user == community.leader:
                # get receiver from request
                    receiver_name = data.get("receiver")
                    pesan = data.get("pesan")
                # get community
                    community = Community.objects.get(nama_community=nama_community)
                # get receiver
                    receiver = User.objects.get(username=receiver_name)
                # check if user is already in community
                    if Anggota.objects.filter(community=community, user=receiver).exists():
                        return JsonResponse({"message": "User sudah bergabung dalam community ini"}, status=400)
                    elif CommunityInvitation.objects.filter(community=community, receiver=receiver).exists():
                        return JsonResponse({"message": "User sudah mendapat invitation dari community ini"}, status=400)
                    else:
                # create community invitation
                        community_invitation = CommunityInvitation.objects.create(
                            community=community,
                            receiver=receiver,
                            sender=request.user,
                            pesan=pesan,
                            is_responded=False
                        )
                        community_invitation.save()
                        return JsonResponse({"message": "Invitation berhasil dikirim",
                                             "success": True
                                             }, status=200)
                else:
                    print("User bukan leader dari community ini")
                    return JsonResponse({"message": "User bukan leader dari community ini",
                                         "success": False
                                         }, status=400)
            else:
                print("Community tidak ditemukan")
                return JsonResponse({"message": "Community tidak ditemukan",
                                     "success": False
                                     }, status=400)
        else:
            print("Method not allowed")
            return JsonResponse({"message": "Method not allowed",
                                 "success": False 
                                 }, status=400)
    else:
        print("User belum login")
        return JsonResponse({"message": "User belum login"}, status=400)

@csrf_exempt
def show_all_user(request, community_id):
    if request.user.is_authenticated:
            print(request.body)
            community = Community.objects.get(id=community_id)
            community_members = Anggota.objects.filter(community__id=community_id).values_list('user__username', flat=True)
            invited = CommunityInvitation.objects.filter(community__id=community_id).values_list('receiver__username', flat=True)

            list_user = list(UserProfile.objects.exclude(user__username__in=community_members).exclude(user__username__in=invited).values('user__username', 'bio'))
            print(str(list_user))
            # return all user
            context = {
                    "list_user": list_user,
                    "community": community,
                }
            print(context) 
            return render(request, 'all_user.html', context)
    else:
        return JsonResponse({"Message": "user belum login"}, status=401)
    

    