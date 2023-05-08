from django.db import models


class PostTag(models.Model):
    """Post Tag model
        Join model for the many to many relationship between post and tag
    """
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="posttags")
    tag = models.ForeignKey(
        "Tag", on_delete=models.CASCADE, related_name="posttags")
