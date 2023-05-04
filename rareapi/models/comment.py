from django.db import models

class Comment(models.Model):

    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='comments')
    author= models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=155)
    created_on = models.DateField()