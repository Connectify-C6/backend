from django.shortcuts import render

from .models import Notification

# Create your views here.

def show_notification(request):
    # get notification if Post is liked, disliked
    if request.user.is_authenticated:
        if request.method == "GET":
            user = request.user
            notifications = Notification.objects.filter(user=user)
            
            