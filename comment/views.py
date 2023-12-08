import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Comment, Reply
from community.models import Anggota
from post.models import Post
from notification.models import Notification

def get_comments(request, id):
    data=[]
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post)
    
    for comment in comments:
        data.append({
            "pk" : comment.pk,
            "author" : comment.author.user.username,
            "content" : comment.content,
            "date" : comment.created_at
        })
    return JsonResponse(data, safe=False)

def get_replies(request, id):
    data=[]
    comment = Comment.objects.get(id=id)
    replies = Reply.objects.filter(comment=comment)
    
    for reply in replies:
        data.append({
            "pk" : reply.pk,
            "author" : reply.author.user.username,
            "content" : reply.content,
            "date" : reply.created_at
        })
    return JsonResponse(data, safe=False)

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
    return redirect('')

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
    return redirect('')
    