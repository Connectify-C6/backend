import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Comment, Reply
from community.models import Anggota
from post.models import Post
from notification.models import Notification

def get_comments(post_id):
    data=[]
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    
    for comment in comments:
        data.append({
            "pk" : comment.pk,
            "author" : comment.author.user.username,
            "content" : comment.content,
            "created_at" : comment.created_at,
            "replies" : get_replies(comment.pk)
        })
    return data

def get_replies(comment_id):
    data=[]
    comment = Comment.objects.get(id=comment_id)
    replies = Reply.objects.filter(comment=comment)
    
    for reply in replies:
        data.append({
            "pk" : reply.pk,
            "author" : reply.author.user.username,
            "content" : reply.content,
            "created_at" : reply.created_at
        })
    return data

@csrf_exempt
def create_comment(request, id):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            post = Post.objects.get(pk=id)
            author = Anggota.objects.get(user=user, community=post.community)
            content = (json.loads(request.body)
                       .get('content'))
            
            new_comment = Comment(
                    post    = post,
                    author  = author,
                    content = content,
                )
            new_comment.save()
            
            # update count comment
            post.jumlah_komen += 1
            post.save()
            
            # create notification
            if user != post.author.user:
                notif_to_poster = Notification(
                    user = post.author.user,
                    message = f"Post Anda dikomentari {user.username}",
                    post = post
                    )
                notif_to_poster.save()
            
            return JsonResponse(
                {"message": "Comment berhasil dibuat"}, 
                status=200,
                safe=False)
    else:
        return JsonResponse(
            {"message": "user belum login"}, 
            status=403)

@csrf_exempt
def delete_comment(request, id):
    this_comment = Comment.objects.get(pk=id)
    this_comment.delete()
    return JsonResponse(
            {"message": "Comment berhasil dihapus"}, 
            status=200)

@csrf_exempt
def create_reply(request, id):
    if request.user.is_authenticated:
        this_user = request.user
        if request.method == "POST":
            comment = Comment.objects.get(pk=id)
            author = Anggota.objects.get(user=this_user, community=comment.post.community)
            content = (json.loads(request.body)
                       .get('content'))
            
            new_reply = Reply(
                    comment = comment,
                    author  = author,
                    content = content,
                )
            new_reply.save()
            
            # update count comment
            comment.post.jumlah_komen += 1
            comment.post.save()
            
            # create notification
            if this_user != comment.author.user:
                notif_to_commenter = Notification(
                    user = comment.author.user,
                    message = f"Comment Anda dibalas oleh {this_user.username}",
                    post = comment.post
                    )
                notif_to_commenter.save()
            
            return JsonResponse(
                {"message": "Reply berhasil dibuat"}, 
                status=200)
    else:
        return JsonResponse(
            {"message": "user belum login"}, 
            status=403)

@csrf_exempt
def delete_reply(request, id):
    this_reply = Reply.objects.get(pk=id)
    this_reply.delete()
    return JsonResponse(
            {"message": "Reply berhasil dihapus"}, 
            status=200)
    