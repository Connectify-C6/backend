from django.urls import path
from post.views import *

app_name = 'post'

urlpatterns = [
    path('<str:community_name>/', get_posts_in_community, name='get_posts_in_community'),
    path('<str:community_name>/create/', create_post, name='create_post'),
    path('like/', like_post, name='like_post'),
    path('dislike/', dislike_post, name='dislike_post'),
]