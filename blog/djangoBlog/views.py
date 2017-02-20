from django.shortcuts import render
from .models import *
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.shortcuts import redirect


def index(request):
    article_list = Article.objects.all().order_by('-publish_date')\
                       .annotate(views=Count('view', distinct=True))[:5]
    news = News.objects.all().order_by('-created_date')[:5]

    if str(request.user) != "AnonymousUser":
        if Blog.objects.all().filter(user=request.user).count() != 1:
            print('creating blog')
            blog = Blog(user=request.user)
            blog.save()

    for article_inst in article_list:
        article_inst.tag_list = article_inst.tags.all()
        article_inst.imagesCount = Image.objects.filter(article=article_inst).count()

    template = loader.get_template("index.html")
    context = {
        'articles': article_list,
        'news': news,
    }
    return HttpResponse(template.render(context, request))


def my_blog(request):
    blog_inst = Blog.objects.get(user=request.user)
    return blog(request, blog_inst.id)


def blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    articles = Article.objects.all().filter(blog=blog).order_by('-publish_date').annotate(views=Count('view'))[:5]

    for article in articles:
        article.tag_list = article.tags.all()
        article.imagesCount = Image.objects.filter(article=article).count()

    template = loader.get_template("blog.html")
    context = {
       'articles': articles,
       'blog': blog,
       'header': str(blog.user) + "'s blog",
       'header_url': "/blog/" + str(blog.id),
       'fb_url': "localhost:8000" + request.get_full_path()
    }
    return HttpResponse(template.render(context, request))


def article(request, article_id):
    article_inst = Article.objects.get(pk=article_id)

    if request.method == "POST":
        comment_content = request.POST.get('comment_content')
        comment = Comment(content=comment_content, article=article_inst, user=request.user)
        comment.save()

    article_inst.tag_list = article_inst.tags.all()
    images = Image.objects.all().filter(article=article_inst)
    blog = article_inst.blog
    comments = Comment.objects.all().filter(article=article_inst).order_by('created_date')
    view = View(article=article_inst)
    view.save()
    article_inst.views = View.objects.filter(article=article_inst).count()
    template = loader.get_template("article.html")
    context = {
        'article': article_inst,
        'blog': blog,
        'comments': comments,
        'images': images,
        'header': str(blog.user) + "'s blog",
        'header_url': "/blog/" + str(blog.id),
        'fb_url': "localhost:8000" + request.get_full_path()
    }
    return HttpResponse(template.render(context, request))


def tag(request, tag_id):
    articles = Article.objects.all().filter(tags=tag_id).order_by('-publish_date')
    tag = Tag.objects.get(value=tag_id)
    for article in articles:
        article.tag_list = article.tags.all()
        article.imagesCount = Image.objects.filter(article=article).count()
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


def delete_article(request):
    if request.method == "GET":
        return redirect("/")

    id = request.POST.get('id')
    article = Article.objects.get(id=id)
    if article.blog.user == request.user:
        article.delete()

    return redirect("/profile")

def add_article(request):
    user = request.user
    if str(user) is "AnonymousUser":
        return redirect("/accounts/login")

    blog = Blog.objects.get(user=user)
    tags = Tag.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        image_desc = request.POST.get('image1Desc')
        image = request.POST.get('image1')
        new_article = Article(title=title, content=content, blog=blog)
        new_article.save()
        tags = list(set(request.POST.getlist('tags[]')))
        for tag in tags:
            if not Tag.objects.filter(value=tag).exists():
                Tag(tag).save()

            tag_inst = Tag.objects.get(value=tag)
            new_article.tags.add(tag_inst)

        if image_desc is not None and len(request.FILES) != 0:
            img_data = request.FILES['image1']
            img = Image(description=image_desc)
            img.save()
            img.image = img_data
            img.save()
            new_article.images.add(img)

        new_article.save()

        return redirect("/profile")

    if request.method == "GET":
        template = loader.get_template("add_article.html")
        context = {
            'blog': blog,
            'tags': tags
        }

        return HttpResponse(template.render(context, request))
