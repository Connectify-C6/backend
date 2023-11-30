from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    bio = models.TextField(max_length=500, blank=True)
    count_reported = models.IntegerField(default=0)
    def get_data(self):
        return {
            "username": self.user.username,
            "role": self.role,
            "bio": self.bio,
            "count_reported": self.count_reported,
            "id": self.user.id
        }