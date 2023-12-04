from django.urls import path
from .views import *

app_name = 'comment'

urlpatterns = [
    path('get-comments/<int:id>/', get_comments, name='get_comments'),
    path('get-comment-replies/<int:id>/', get_replies, name='get_replies'),
    path('add-comment/<int:id>/', create_comment, name='create_comment'),
    path('add-reply/<int:id>/', create_reply, name='create_reply'),
    path('delete-comment/<int:id>/', delete_comment, name='delete_comment'),
    path('delete-reply/<int:id>/', delete_reply, name='delete_reply'),
]