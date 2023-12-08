from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Post
from community.models import Community, Anggota
from login.models import UserProfile
from notification.models import Notification
import json

def get_posts_in_community(request, community_name):
    if request.method == "GET":
        data = []
        community = Community.objects.get(nama_community=community_name)
        posts = Post.objects.filter(community=community)
        
        for post in posts:
            data.append({
            "pk" : post.pk,
            "author" : post.author.user.username,
            "isi" : post.isi,
            "jumlah_like" : post.jumlah_like,
            "jumlah_dislike" : post.jumlah_dislike,
            "jumlah_komen" : post.jumlah_komen,
            "created_at" : post.created_at,
        })
        return JsonResponse(data, safe=False)

@csrf_exempt
def create_post(request, community_name):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            isi = data.get("isi")
            community = Community.objects.get(nama_community=community_name)  # Get community ID from request data
            author = request.user

            # Check if author is a member of the specified community
            if Anggota.objects.filter(user=author, community=community).exists():
                anggota = Anggota.objects.get(user=author, community=community)
                post = Post.objects.create(
                    isi=isi,
                    author=anggota,
                    community=community
                )
                return JsonResponse({"message": "Post berhasil dibuat",
                                    "isi": post.isi,
                                    "author": post.author.user.username,
                                    }, status=200)
            else:
                return JsonResponse({"message": "Anda bukan anggota atau komunitas tidak ditemukan"}, status=400)
    else:
        return JsonResponse({"message": "user belum login"}, status=400)
    
@csrf_exempt
def like_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            post_id = data.get("post_id")
            post = Post.objects.get(id=post_id)
            author = request.user
            
            
            community_id = data.get("community_id")  # Get community ID from request data
            anggota_author = Anggota.objects.get(user=author, community_id=community_id)

            # check jika user sudah like post
            if post.daftar_like.filter(user=author).exists() and Anggota.objects.filter(user=author, community_id=community_id).exists():
                post.daftar_like.remove(anggota_author)
                post.jumlah_like -= 1
                post.save()
                Notification.objects.filter(user=author, post_id=post).delete()
                return JsonResponse({"message": "Post disliked"}, status=200)
            # cek jika kondisi awalnya user dislike post
            elif post.daftar_dislike.filter(user=author).exists() and Anggota.objects.filter(user=author, community_id=community_id).exists():
                post.daftar_dislike.remove(anggota_author)
                post.daftar_like.add(anggota_author)
                post.jumlah_like += 1
                post.jumlah_dislike -= 1
                post.save()
                # send message to notification jika post di like
                message = "Post anda di like oleh " + author.username
                if Notification.objects.filter(user=post.author.user, post_id=post.id, message=message).exists():
                    Notification.objects.filter(user=post.author.user, post_id=post.id, message=message).delete()
                if post.author.user != author:
                    Notification.objects.create(
                        user=post.author.user,
                        message=message,
                        post_id=post.id,
                    )
                return JsonResponse({"message": "Post liked"}, status=200)
            else:
                post.daftar_like.add(anggota_author)
                post.jumlah_like += 1
                post.save()
                message = "Post anda di like oleh " + author.username
                if Notification.objects.filter(user=post.author.user, post_id=post.id, message=message).exists():
                    Notification.objects.filter(user=post.author.user, post_id=post.id, message=message).delete()
                if post.author.user != author:
                    Notification.objects.create(
                        user=post.author.user,
                        message=message,
                        post_id=post.id,
                    )
                return JsonResponse({"message": "Post liked"}, status=200)
    else:
        return JsonResponse({"message": "user belum login"}, status=400)
    
@csrf_exempt
def dislike_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body)
            post_id = data.get("post_id")
            post = Post.objects.get(id=post_id)
            author = request.user
            
            community_id = data.get("community_id")
            anggota_author = Anggota.objects.get(user=author, community_id=community_id)

            # check jika user sudah dislike post
            if post.daftar_dislike.filter(user=author).exists() and Anggota.objects.filter(user=author, community_id=community_id).exists():
                post.daftar_dislike.remove(anggota_author)
                post.jumlah_dislike -= 1
                post.save()
                Notification.objects.filter(user=author, post_id=post).delete()
                return JsonResponse({"message": "Post undisliked"}, status=200)
            
            # cek jika kondisi awalnya user like post
            elif post.daftar_like.filter(user=author).exists() and Anggota.objects.filter(user=author, community_id=community_id).exists():
                post.daftar_like.remove(anggota_author)
                post.daftar_dislike.add(anggota_author)
                post.jumlah_like -= 1
                post.jumlah_dislike += 1
                post.save()
                message = "Post anda di dislike oleh " + author.username
                if Notification.objects.filter(user=post.author.user, post_id=post.id, message=message).exists():
                    Notification.objects.filter(user=post.author.user, post_id=post.id, message=message).delete()
                # jika yang like post adalah author, maka tidak perlu ada notifikasi
                if post.author.user != author:
                    Notification.objects.create(
                        user=post.author.user,
                        message=message,
                        post_id=post.id,
                    )
                return JsonResponse({"message": "Post disliked"}, status=200)
            else:
                post.daftar_dislike.add(anggota_author)
                post.jumlah_dislike += 1
                post.save()
                message = "Post anda di dislike oleh " + author.username
                if Notification.objects.filter(user=post.author.user, post_id=post.id, message=message).exists():
                    Notification.objects.filter(user=post.author.user, post_id=post.id, message=message).delete()
                if post.author.user != author:
                    Notification.objects.create(
                        user=post.author.user,
                        message=message,
                        post_id=post.id,
                    )
                return JsonResponse({"message": "Post disliked"}, status=200)
    else:
        return JsonResponse({"message": "user belum login"}, status=400)