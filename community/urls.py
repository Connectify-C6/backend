from django.urls import path
from community.views import *
from post.views import show_community

app_name = 'community'

urlpatterns = [
    path('', index, name='index'),
    path('create/', create_community, name='create_community'),
    # GET community member with member id 
    path('<int:community_id>/member/', get_community_member, name='get_community_member'),
    #path('<int:community_id>/detail/', show_community_detail, name='show_community_detail'),
    # join community
    path('join/', join_community, name='join_community'),
    # send invitation
    path('invite/', send_invitation, name='send_invitation'),
    path('<str:community_name>/', show_community, name='show_community'),
]