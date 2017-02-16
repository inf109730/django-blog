from django.contrib import admin
from .models import *


class BlogAdmin(admin.ModelAdmin):
    list_display = ('user', 'header', 'about', 'style')


class TagAdmin(admin.ModelAdmin):
    list_display = ('value',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('description', 'image')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'publish_date', 'blog')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'content', 'created_date')


class ViewAdmin(admin.ModelAdmin):
    list_display = ('view_date', 'article')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_date')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(News, NewsAdmin)

