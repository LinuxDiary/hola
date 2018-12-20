"""hola URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from articles.views import IndexView, ArticleDetailView, ArticleListView, ArticleSearchView
from comments.views import CommentsView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^favicon.ico$', RedirectView.as_view(url='static/favicon.ico')),
    re_path(r'mdeditor/', include('mdeditor.urls')),
    path('', IndexView.as_view(), name='index'),
    path('category/<str:name>/', ArticleListView.as_view(), name='cate_list'),
    path('tag/<str:name>/', ArticleListView.as_view(), name='tag_list'),
    path('<str:short_title>/', ArticleDetailView.as_view(), name='detail'),
    re_path(r'^comment', CommentsView.as_view(), name='comment'),
    re_path(r'^search', ArticleSearchView.as_view(), name='search')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
