from django.db import models
from django.contrib.auth.models import User

class Subscription(models.Model):
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='subscribedTo')
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='subscribers')
    created_on = models.DateField()