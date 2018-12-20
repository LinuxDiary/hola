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


class ArticleBaseView(View):
    categories = Category.objects.filter(parent_cate=None).exclude(id=1)
    hot_posts = Post.get_hot_posts()
    all_tags = Tag.objects.all()

    context = {
        'categories': categories,
        'hot_posts': hot_posts,
        'all_tags': all_tags,
    }


class IndexView(ArticleBaseView):
    def get(self, request):
        self.context.update(
            current_page='index',
            banner_posts=Post.get_banner_posts()
        )

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        all_posts = Post.objects.all().order_by('-create_time')
        p = Paginator(all_posts, 3)
        posts = p.page(page)
        self.context.update(posts=posts)

        return render(request, 'article/index.html', self.context)


class ArticleDetailView(ArticleBaseView):
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

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        comments = Comments.objects.filter(post=post)
        p = Paginator(comments, 10)
        comment_list = p.page(page)
        self.context.update(comment_list=comment_list)

        return render(request, 'article/page.html', self.context)

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


class ArticleListView(ArticleBaseView):
    def get(self, request, name):
        if Category.objects.filter(short_name=name):
            obj = get_object_or_404(Category, short_name=name)
            posts_list = obj.get_category_posts()
        elif Tag.objects.filter(name=name):
            obj = get_object_or_404(Tag, name=name)
            posts_list = obj.get_tag_posts()
        else:
            return Http404

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(posts_list, 3)
        posts = p.page(page)
        self.context.update(keyword=obj, posts=posts)

        return render(request, 'article/category.html', self.context)


class ArticleSearchView(ArticleBaseView):
    def get(self, request):
        q = request.GET.get('q', '')
        results = Post.objects.filter(
            Q(title__icontains=q) |
            Q(excerpt__icontains=q) |
            Q(content__icontains=q)
        )

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(results, 3)
        posts = p.page(page)
        self.context.update(keyword=q, posts=posts)

        return render(request, 'article/category.html', self.context)
