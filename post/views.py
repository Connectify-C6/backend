from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Post
from community.models import Community, Anggota
from login.models import UserProfile
import json

@csrf_exempt
def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            isi = data.get("isi")
            community_id = data.get("community_id")  # Get community ID from request data
            author = request.user

            # Check if author is a member of the specified community
            if Anggota.objects.filter(user=author, community_id=community_id).exists():
                anggota = Anggota.objects.get(user=author, community_id=community_id)
                post = Post.objects.create(
                    isi=isi,
                    author=anggota,
                )
                return JsonResponse({"message": "Post berhasil dibuat",
                                    "isi": post.isi,
                                    "author": post.author.user.username,
                                    }, status=200)
            else:
                return JsonResponse({"message": "Anda bukan anggota atau komunitas tidak ditemukan"}, status=400)
    else:
        return JsonResponse({"message": "user belum login"}, status=400)

            