import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from articles.models import Post
from .models import Comments
from .forms import CommentsForm


class CommentsView(View):
    def get(self, request):
        pass

    def post(self, request):
        """评论提交"""
        post = get_object_or_404(Post, id=request.POST.get('post_id', 0))
        try:
            reply_to = Comments.objects.get(id=int(request.POST.get('comment_id', 0)))
        except Exception as e:
            # print(e.args)
            reply_to = None
        form = CommentsForm(request.POST)
        content = re.sub(r'^@.*?\n', '', request.POST.get('content'))
        if form.is_valid():
            Comments.objects.create(
                content=content,
                author=request.POST.get('author', ''),
                email=request.POST.get('email', ''),
                post=post,
                reply_to=reply_to
            )
            res = {
                'status': True,
                'msg': '评论成功'
            }
        else:
            res = {
                'status': False,
                'msg': '评论不符合规范，请重新输入',
                'error': form.errors
            }
        return JsonResponse(res)
