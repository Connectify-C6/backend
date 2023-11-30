from django.urls import path
from notification.views import *

app_name = 'notification'

urlpatterns = [
    path('', show_notification, name='show_notification'),
]