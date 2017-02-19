"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from djangoBlog import views as blog
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', blog.index, name="index"),  # main page
    url(r'^profile/$', blog.profile, name="user_profile"),  # user's blog setting
    url(r'^blog/$', blog.my_blog, name="my_blog"),  # blog
    url(r'^blog/(?P<blog_id>\d+)/$', blog.blog, name="another_blog"),  # blog
    url(r'^article/(?P<article_id>\d+)/$', blog.article, name="article"),   # article
    url(r'^tag/(?P<tag_id>[\w|\W]+)/$', blog.tag, name="tag"),    # tag
    url(r'^add-article', blog.add_article, name="add_article"),    # add article
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
