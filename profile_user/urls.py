from django.urls import path
from profile_user.views import *

app_name = 'profile_user'

urlpatterns = [
    path('', index, name='index'),
    path('<str:username>/', get_profile_by_username, name='get_profile_by_username'),
    path('update/<str:username>/', update_profile, name='update_profile')
]