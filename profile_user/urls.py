from django.urls import path
from profile_user.views import *

app_name = 'profile_user'

urlpatterns = [
    path('', index, name='index'),
    path('<str:username>/', show_profile_by_username, name='show_profile_by_username'),
]