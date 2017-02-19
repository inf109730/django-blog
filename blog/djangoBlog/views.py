from django.shortcuts import render
from .models import *
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.shortcuts import redirect


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
    article_inst = Article.objects.get(pk=article_id)
    article_inst.tag_list = article_inst.tags.all()
    blog = article_inst.blog
    view = View(article=article_inst)
    view.save()
    article_inst.views = View.objects.filter(article=article_inst).count()
    template = loader.get_template("article.html")
    context = {
        'article': article_inst,
        'blog': blog,
        'header': str(blog.user) + "'s blog",
        'header_url': "/blog/" + str(blog.id)
    }
    return HttpResponse(template.render(context, request))


def tag(request, tag_id):
    articles = Article.objects.all().filter(tags=tag_id).order_by('-publish_date')
    tag = Tag.objects.get(id=tag_id)
    template = loader.get_template("tag.html")
    context = {
        'articles': articles,
        'tag': tag
    }
    return HttpResponse(template.render(context, request))


def profile(request):
    user = request.user
    if str(user) is "AnonymousUser":
        return redirect("/accounts/login")
    blog = Blog.objects.get(user=user)
    articles = Article.objects.filter(blog=blog).order_by('-publish_date')

    for article in articles:
        article.tag_list = article.tags.all()
        article.views = View.objects.filter(article=article).count()

    if request.method == "POST":
        blog.style = request.POST.get('style')
        blog.about = request.POST.get('about')
        blog.save()

    template = loader.get_template("profile.html")
    context = {
        'blog': blog,
        'style_list': [tup[0] for tup in Blog.STYLES],
        'articles': articles
    }

    if request.method == "POST":
        context['saved'] = True

    return HttpResponse(template.render(context, request))


def add_article(request):
    user = request.user
    if str(user) is "AnonymousUser":
        return redirect("/accounts/login")

    blog = Blog.objects.get(user=user)

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags')

        return redirect("/blog")

    if request.method == "GET":
        template = loader.get_template("add_article.html")
        context = {
            'blog': blog
        }

        return HttpResponse(template.render(context, request))
