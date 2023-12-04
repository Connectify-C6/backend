from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from community.models import Community

class Invitation(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    pesan = models.TextField()
    is_responded = models.BooleanField()

class CommunityInvitation(Invitation):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_community = models.CharField(max_length=255, editable=False)

    def save(self, *args, **kwargs):
        self.nama_community = self.community.nama_community
        super().save(*args, **kwargs)
        
class FriendRequest(Invitation):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
