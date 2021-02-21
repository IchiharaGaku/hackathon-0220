from django.db import models
from django.utils import timezone

# Create your models here.

class Article(models.Model):

    movie_name = models.CharField(max_length=200, default="")
    thumb_frame = models.IntegerField(default=0)
    upload_file_name = models.CharField(max_length=200, default="")
    content = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)


    
