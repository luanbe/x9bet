from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    description = models.CharField(max_length=1000, null=True)
    image_feature = models.CharField(max_length=1000, null=True)
    # pub_date = models.DateTimeField("date published", auto_now=True)
    url_crawl = models.CharField(max_length=1000, null=True)
