from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Blog(models.Model):
    user = models.OneToOneField(User, related_name="account")
    header = models.ImageField(default='blank_header.jpg')
    about = models.TextField(null=True, blank=True)


class Tag(models.Model):
    value = models.CharField(max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    blog = models.ForeignKey(Blog)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)


class View(models.Model):
    view_date = models.DateTimeField(default=timezone.now)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
