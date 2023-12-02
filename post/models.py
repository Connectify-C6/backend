from django.db import models
from community.models import Community, Anggota
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    isi = models.TextField()
    author = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    jumlah_direport = models.IntegerField(
        default=0,
    )
    jumlah_like = models.IntegerField(
        default=0,
    )
    jumlah_dislike = models.IntegerField(
        default=0,
    )
    jumlah_komen = models.IntegerField(
        default=0,
    )
    jumlah_direport = models.IntegerField(
        default=0,
    )
    daftar_like = models.ManyToManyField(Anggota, related_name='daftar_like')
    daftar_dislike = models.ManyToManyField(Anggota, related_name='daftar_dislike')
    created_at = models.DateTimeField(auto_now_add=True)

