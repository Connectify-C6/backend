from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification

# Create your views here.

def show_notification(request):
    # get notification if Post is liked, disliked
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            notifications = Notification.objects.filter(user=user)
            return JsonResponse({"message": "Berhasil mendapatkan notifikasi",
                                "notifications": list(notifications.values())}, status=200)
    else:
        return JsonResponse({"message": "user belum login"}, status=400)
    

            