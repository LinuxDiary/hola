from markdown import markdown
from datetime import datetime
import hashlib

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from pure_pagination import Paginator, PageNotAnInteger

from .models import Post, Category, Tag
from comments.models import Comments


class IndexView(View):
    def get(self, request):
        current_page = 'index'
        hot_posts = Post.get_hot_posts()
        category_in_nav = Category.objects.all().exclude(id=1)
        categories = category_in_nav.filter(parent_cate=None)
        all_posts = Post.objects.all().order_by('-create_time')
        all_tags = Tag.objects.all()
        banner_posts = Post.get_banner_posts()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_posts, per_page=2)
        posts = p.page(page)

        return render(request, 'article/index.html', {
            'category_in_nav': category_in_nav,
            'categories': categories,
            'posts': posts,
            'hot_posts': hot_posts,
            'banner_posts': banner_posts,
            'all_tags': all_tags,
            'current_page': current_page,
        })


class ArticleDetailView(View):
    def get(self, request, short_title):
        hot_posts = Post.get_hot_posts()
        categories = Category.objects.filter(parent_cate=None).exclude(id=1)
        post = get_object_or_404(Post, short_title=short_title)
        comment_list = Comments.objects.filter(post=post)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(comment_list, 10)
        comments = p.page(page)

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
        return render(request, 'article/page.html', {
            'post': post,
            'comment_list': comments,
            'hot_posts': hot_posts,
            'categories': categories
        })

    def post(self, request, short_title):
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


class ArticleCategoryView(View):
    def get(self, request, short_name):
        category = get_object_or_404(Category, short_name=short_name)
        posts_in_category = category.get_category_posts()
        hot_posts = Post.get_hot_posts()
        all_tags = Tag.objects.all()
        categories = Category.objects.filter(parent_cate=None).exclude(id=1)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(posts_in_category, 2)
        posts = p.page(page)

        return render(request, 'article/category.html', {
            'keyword': category,
            'posts': posts,
            'hot_posts': hot_posts,
            'all_tags': all_tags,
            'categories': categories
        })


class ArticleTagView(View):
    def get(self, request, tag_name):
        tag = get_object_or_404(Tag, name=tag_name)
        posts_in_tag = tag.get_tag_posts()
        hot_posts = Post.get_hot_posts()
        all_tags = Tag.objects.all()
        categories = Category.objects.filter(parent_cate=None).exclude(id=1)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(posts_in_tag, 2)
        posts = p.page(page)

        return render(request, 'article/category.html', {
            'keyword': tag,
            'posts': posts,
            'hot_posts': hot_posts,
            'all_tags': all_tags,
            'categories': categories
        })


class ArticleSearchView(View):
    def get(self, request):
        q = request.GET.get('q', '')
        results = Post.objects.filter(
            Q(title__icontains=q) |
            Q(excerpt__icontains=q) |
            Q(content__icontains=q)
        )
        hot_posts = Post.get_hot_posts()
        categories = Category.objects.filter(parent_cate=None).exclude(id=1)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(results, 2)
        posts = p.page(page)

        return render(request, 'article/category.html', {
            'keyword': q,
            'posts': posts,
            'hot_posts': hot_posts,
            'categories': categories
        })
