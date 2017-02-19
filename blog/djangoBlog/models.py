from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Blog(models.Model):
    STYLES = (
        ('Cerulean', 'Cerulean'),
        ('Darkly', 'Darkly'),
        ('Superhero', 'Superhero'),
        ('Cosmo', 'Cosmo'),
        ('Slate', 'Slate'),
    )
    user = models.OneToOneField(User, related_name="account")
    header = models.ImageField(default='blank_header.jpg')
    about = models.TextField(null=True, blank=True)
    style = models.CharField(max_length=20, choices=STYLES, default="Cerulean")


class Tag(models.Model):
    value = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.value


class Image(models.Model):
    description = models.CharField(max_length=200)
    image = models.ImageField()

    def __str__(self):
        return self.description


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    images = models.ManyToManyField(Image)
    blog = models.ForeignKey(Blog)

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title
