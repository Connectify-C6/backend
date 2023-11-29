from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Community(models.Model):
    nama_community = models.CharField(max_length=50)
    detail_community = models.TextField()
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    jumlah_anggota = models.IntegerField()
    jumlah_direport = models.IntegerField()