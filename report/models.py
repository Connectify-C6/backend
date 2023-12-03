from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    id_report = models.AutoField(primary_key=True)
    reported_user = models.ForeignKey(User, related_name='reported_user', on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, related_name='reporter', on_delete=models.CASCADE)
    # reported_post = models.ForeignKey('yourapp.Post', null=True, blank=True, on_delete=models.CASCADE)
    reason = models.TextField()
    # reported_community = models.ForeignKey('yourapp.Community', null=True, blank=True, on_delete=models.CASCADE)
