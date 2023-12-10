from django.urls import path
from post.views import *

app_name = 'post'

urlpatterns = [
    path('<str:community_name>/<int:id>/', show_post_detail, name='show_post_detail'),
    path('<str:community_name>/create/', create_post, name='create_post'),
    path('<int:post_id>/like/', like_post, name='like_post'),
    path('<int:post_id>/dislike/', dislike_post, name='dislike_post'),
]