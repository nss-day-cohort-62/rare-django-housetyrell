from django.db import models



class Post(models.Model):

    user= models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey("Category", null=True, blank=True, on_delete=models.SET_NULL, related_name='posts' )
    title = models.CharField(max_length=155)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=155)
    content = models.CharField(max_length=155)
    approved= models.BooleanField()

   