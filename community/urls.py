from django.urls import path
from community.views import *

app_name = 'community'

urlpatterns = [
    path('', index, name='index'),
    path('create/', create_community, name='create_community'),
    # GET community member
    path('<str:nama_community>/member/', get_community_member, name='get_community_member'),
    # join community
    path('<str:nama_community>/join/', join_community, name='join_community'),
]