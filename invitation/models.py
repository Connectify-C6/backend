from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from community.models import Community

class Invitation(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    pesan = models.TextField()

class CommunityInvitation(Invitation):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

class FriendRequest(Invitation):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)