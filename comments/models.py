from django.db import models
from django.template.defaultfilters import truncatechars

from articles.models import Post


class Comments(models.Model):
    author = models.CharField(max_length=20, verbose_name='评论作者')
    email = models.EmailField(max_length=50, default='', blank=True, verbose_name='邮箱')
    website = models.URLField(max_length=150, default='', blank=True, verbose_name='网页')
    content = models.TextField(blank=False, verbose_name='评论内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    reply_to = models.ForeignKey(
        'self',
        related_name='reply',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='向他回复'
    )

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        db_table = 'comments'

    def __str__(self):
        return self.author

    @property
    def short_content(self):
        return truncatechars(self.content, 30)
