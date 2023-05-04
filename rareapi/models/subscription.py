from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='subscriptions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    created_on = models.DateField()
    ended_on = models.DateField()