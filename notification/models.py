from django.db import models
from django.contrib.auth.models import User
from post.models import Post

# Create your models here.

class Notification(models.Model):
    # 1. Notification for post
    # 2. Notification for comment

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

