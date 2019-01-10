from markdown import markdown
import hashlib

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from pure_pagination import Paginator, PageNotAnInteger

from .models import Post, Category, Tag
from comments.models import Comments


def results_pagination(request, queryset, per_page):
    """返回分页的 queryset"""
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(queryset, per_page)
    return p.page(page)


class ArticleBaseView(View):
    """公共的 context"""
    def __init__(self, **kwargs):
        super(ArticleBaseView, self).__init__(**kwargs)
        self.categories = Category.objects.filter(parent_cate=None).exclude(id=1)
        self.hot_posts = Post.get_hot_posts()
        self.all_tags = Tag.objects.all()

        self.context = {
            'categories': self.categories,
            'hot_posts': self.hot_posts,
            'all_tags': self.all_tags,
        }


class IndexView(ArticleBaseView):
    """首页视图"""
    def get(self, request):
        self.context.update(
            current_page='index',
            banner_posts=Post.get_banner_posts()
        )

        posts = results_pagination(request, Post.objects.all().order_by('-create_time'), 3)
        self.context.update(posts=posts)

        return render(request, 'article/index.html', self.context)


class ArticleDetailView(ArticleBaseView):
    """详情页视图"""
    def get(self, request, short_title):
        post = get_object_or_404(Post, short_title=short_title)
        self.context.update(post=post)

        post.views += 1
        post.save()
        post.content = markdown(
            post.content,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )

        comment_list = results_pagination(request, Comments.objects.filter(post=post), 10)
        self.context.update(comment_list=comment_list)
        return render(request, 'article/page.html', self.context)

    def post(self, request, short_title):
        """点赞功能"""
        post = get_object_or_404(Post, short_title=short_title)
        hash_id = hashlib.sha1(str(post.create_time).encode('utf-8')).hexdigest()
        res = {'status': 1, 'msg': ''}
        try:
            if hash_id in str(request.COOKIES.get(short_title)):
                res['status'] = 0
                res['msg'] = '已经赞过啦'
                return JsonResponse(res)
            else:
                post.likes += 1
                post.save()
                res['msg'] = post.likes
                response = JsonResponse(res)
                response.set_signed_cookie(short_title, value=hash_id, max_age=86400)
                return response
        except ObjectDoesNotExist:
            raise Http404


class ArticleListView(ArticleBaseView):
    """文章列表"""
    def get(self, request, name):
        if Category.objects.filter(short_name=name):
            obj = get_object_or_404(Category, short_name=name)
            posts_list = obj.get_category_posts()
        elif Tag.objects.filter(name=name):
            obj = get_object_or_404(Tag, name=name)
            posts_list = obj.get_tag_posts()
        else:
            raise Http404

        posts = results_pagination(request, posts_list, 3)
        self.context.update(keyword=obj, posts=posts)

        return render(request, 'article/category.html', self.context)


class ArticleSearchView(ArticleBaseView):
    """简单搜索"""
    def get(self, request):
        q = request.GET.get('q', '')
        results = Post.objects.filter(
            Q(title__icontains=q) |
            Q(excerpt__icontains=q) |
            Q(content__icontains=q)
        )

        posts = results_pagination(request, results, 3)
        self.context.update(keyword=q, posts=posts)

        return render(request, 'article/category.html', self.context)
