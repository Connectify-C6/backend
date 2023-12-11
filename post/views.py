from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Post
from community.models import Community, Anggota
from login.models import UserProfile
from notification.models import Notification
from comment.views import get_comments
from django.db import transaction
import json
from django.shortcuts import get_object_or_404

def get_posts_in_community(community_name):
    data = []
    community = Community.objects.get(nama_community=community_name)
    posts = Post.objects.all().filter(community=community).order_by("-created_at")
    
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
    return data

def show_community(request, community_name):
    community = Community.objects.get(nama_community=community_name)
    posts = get_posts_in_community(community_name=community_name)
    
    context = {
        'community' : community,
        'posts' : posts,
        'user' : request.user
    }
    return render(request,'show_community_posts.html',context)

def show_post_detail(request, community_name, id):
    community = get_object_or_404(Community, nama_community=community_name)
    post = Post.objects.get(id=id)
    context = {
        'community' : community,
        'post' : post,
        'comments' : get_comments(id),
        'user' : request.user
    }
    return render(request, 'detail_post.html', context)

@csrf_exempt
def create_post(request, community_name):
    if request.user.is_authenticated:
        if request.method == "POST":
            isi = request.POST.get("isi")
            community = Community.objects.get(nama_community=community_name)
            author = request.user

            # Check if author is a member of the specified community
            if Anggota.objects.filter(user=author, community=community).exists():
                anggota = Anggota.objects.get(user=author, community=community)
                post = Post.objects.create(
                    isi=isi,
                    author=anggota,
                    community=community
                )
                return JsonResponse({
                    "message": "Post berhasil dibuat",
                    "isi": post.isi,
                    "author": post.author.user.username,
                    "post_id": post.id  # Assuming you have an ID field
                }, status=200)
            else:
                return JsonResponse({"message": "Anda bukan anggota atau komunitas tidak ditemukan"}, status=400)
    else:
        return JsonResponse({"message": "User belum login"}, status=400)



@csrf_exempt
def like_post(request, post_id):
    if request.user.is_authenticated and request.method == "POST":
        data = json.loads(request.body)
        community_id = data.get("community_id")
        author = request.user

        try:
            with transaction.atomic():
                post = Post.objects.get(id=post_id)
                anggota_author = Anggota.objects.get(user=author, community_id=community_id)
                already_disliked = post.daftar_dislike.filter(user=author).exists()
                if already_disliked:
                    post.daftar_dislike.remove(anggota_author)
                    post.jumlah_dislike -= 1

                if post.daftar_like.filter(user=author).exists():
                    post.daftar_like.remove(anggota_author)
                    post.jumlah_like -= 1
                    post.save()
                    Notification.objects.filter(user=author, post_id=post).delete()
                    return JsonResponse({"message": "Post unliked", "new_like_count": post.jumlah_like, "new_dislike_count": post.jumlah_dislike}, status=200)
                else:
                    post.daftar_like.add(anggota_author)
                    post.jumlah_like += 1
                    post.save()
                    # Check and update or create notification
                    notification, created = Notification.objects.get_or_create(
                        user=post.author.user,
                        post_id=post.id,
                        defaults={'message': f"Post anda di like oleh {author.username}"}
                    )
                    if not created:
                        notification.message = f"Post anda di like oleh {author.username}"
                        notification.save()
                    return JsonResponse({"message": "Post liked", "new_like_count": post.jumlah_like, "new_dislike_count": post.jumlah_dislike}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({"message": "Post not found"}, status=404)
        except Anggota.DoesNotExist:
            return JsonResponse({"message": "Anggota not found"}, status=404)

    else:
        return JsonResponse({"message": "User not logged in"}, status=400)
    
@csrf_exempt
def dislike_post(request, post_id):
    if request.user.is_authenticated and request.method == "POST":
        data = json.loads(request.body)
        community_id = data.get("community_id")
        author = request.user

        try:
            with transaction.atomic():
                post = Post.objects.get(id=post_id)
                anggota_author = Anggota.objects.get(user=author, community_id=community_id)
                # Check if the user has liked this post before
                already_liked = post.daftar_like.filter(user=author).exists()
                if already_liked:
                    post.daftar_like.remove(anggota_author)
                    post.jumlah_like -= 1
                if post.daftar_dislike.filter(user=author).exists():
                    post.daftar_dislike.remove(anggota_author)
                    post.jumlah_dislike -= 1
                    post.save()
                    Notification.objects.filter(user=author, post_id=post).delete()
                    return JsonResponse({"message": "Post undisliked", "new_like_count": post.jumlah_like, "new_dislike_count": post.jumlah_dislike}, status=200)
                else:
                    post.daftar_dislike.add(anggota_author)
                    post.jumlah_dislike += 1
                    post.save()
                    # Check and update or create notification
                    notification, created = Notification.objects.get_or_create(
                        user=post.author.user,
                        post_id=post.id,
                        defaults={'message': f"Post anda di dislike oleh {author.username}"}
                    )
                    if not created:
                        notification.message = f"Post anda di dislike oleh {author.username}"
                        notification.save()
                    return JsonResponse({"message": "Post disliked", "new_like_count": post.jumlah_like, "new_dislike_count": post.jumlah_dislike}, status=200)

        except Post.DoesNotExist:
            return JsonResponse({"message": "Post not found"}, status=404)
        except Anggota.DoesNotExist:
            return JsonResponse({"message": "Anggota not found"}, status=404)

    else:
        return JsonResponse({"message": "User not logged in"}, status=400)