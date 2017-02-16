from django.shortcuts import render
from .models import *
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count


def index(request):
    article_list = Article.objects.all().annotate(views=Count('view'))[:5]
    news = News.objects.all()[:5]

    for article_inst in article_list:
        article_inst.tag_list = article_inst.tags.all()

    template = loader.get_template("index.html")
    context = {
        'articles': article_list,
        'news': news,
    }
    return HttpResponse(template.render(context, request))


def user_blog(request):
    pass


def another_blog(request, blog_id):
    pass


def article(request, article_id):
    article_inst = Article.objects.get(pk=article_id)\
        .annotate(views=Count('view'))
    view = View(article=article_inst)
    view.save()
    template = loader.get_template("article.html")
    context = {
        'article': article_inst
    }
    return HttpResponse(template.render(context, request))

def tag(request, tag_name):
    pass