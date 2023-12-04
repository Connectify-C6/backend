from django.urls import path
from invitation.views import *

app_name = 'invitation'

urlpatterns = [
    path('', index, name='index'),
    path('accept/', accept_community_invitation, name='accept_community_invitation'),
    path('decline/', decline_community_invitation, name='decline_community_invitation'),
    ]