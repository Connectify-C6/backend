from django.shortcuts import render
# import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Community, Anggota
from login.models import UserProfile
# import json
from rest_framework.parsers import JSONParser
import json
# Create your views here.

def index(request):
    # check if user is authenticated
    if request.user.is_authenticated:
        # if method is post
        list_community = list(Community.objects.all().values_list('nama_community', flat=True))
        return JsonResponse({"Message":"Hello World",
                         "User":request.user.username,
                         "list_community": list_community
                         }, status=200)
                         
    else:
        return JsonResponse({"Message":"user belum login"}, status=400)


@csrf_exempt
def create_community(request):
    # check if user is authenticated
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
def join_community(request, nama_community):
    # check if user is authenticated
    if request.user.is_authenticated:
        # if method is post
        if request.method == "POST":
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

def get_community_member(request, nama_community):
    # check if user is authenticated
    if request.user.is_authenticated:
        # if method is post
        if request.method == "GET":
            # get community
            community = Community.objects.get(nama_community=nama_community)
            # get all anggota from community
            anggota = Anggota.objects.filter(community=community)
            # get all user from anggota
            user = UserProfile.objects.filter(user__in=anggota.values_list('user', flat=True))
            # return all user
            return JsonResponse({"message": "Berhasil mendapatkan semua anggota",
                                 "nama_community": community.nama_community,
                                 "leader": community.leader.username,
                                 "anggota": list(user.values_list('user__username', flat=True))
                                 }, status=200)
        else:
            return JsonResponse({"message": "Method not allowed"}, status=400)
    else:
        return JsonResponse({"message": "User belum login"}, status=400)