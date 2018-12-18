from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from mdeditor.fields import MDTextField


class BaseModelArticle(models.Model):
    """基础类"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        abstract = True


class Category(BaseModelArticle):
    """分类"""
    name = models.CharField(max_length=20, blank=False, null=False, verbose_name='分类')
    show_in_nav = models.BooleanField(default=False, verbose_name='是否显示在首页次导航中')
    short_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        unique=True,
        verbose_name='自定义链接'
    )
    parent_cate = models.ForeignKey(
        'self',
        related_name='child',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='父级分类'
    )

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_child_cates(self):
        return self.child.all()

    def get_category_posts(self):
        return self.post_set.all()

    def get_category_posts_counts(self):
        return self.post_set.all().count()

    get_category_posts_counts.short_description = '文章数'


class Tag(BaseModelArticle):
    """标签"""
    name = models.CharField(max_length=20, default='', verbose_name='标签')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_tag_posts(self):
        return self.post_set.all()


class SystemRequirement(BaseModelArticle):
    """软件系统要求"""
    name = models.CharField(max_length=20, default='', verbose_name='软件系统要求')

    class Meta:
        verbose_name = '软件系统要求'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


def get_default_user():
    return User.objects.get(id=1)


def get_default_category():
    if Category.objects.get(id=1):
        Category.objects.get(id=1).delete()
    return Category.objects.get_or_create(id=1, name='未分类', short_name='undefined')


class Post(BaseModelArticle):
    """文章"""
    UNIT_CHOICES = (
        ('m', 'MB'),
        ('g', 'GB')
    )
    title = models.CharField(blank=False, null=False, max_length=100, verbose_name='标题')
    excerpt = models.TextField(default='', blank=True, max_length=200, verbose_name='摘要')
    # content = models.TextField(default='', blank=False, null=False, verbose_name='内容')
    content = MDTextField()
    views = models.IntegerField(default=0, verbose_name='阅读数')
    likes = models.IntegerField(default=0, verbose_name='点赞数')
    is_banner = models.BooleanField(default=False, verbose_name='轮播')
    image = models.ImageField(
        default='default.png',
        max_length=100,
        blank=True,
        null=True,
        upload_to='posts/%Y/%m',
        verbose_name='缩略图'
    )
    short_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        verbose_name='自定义链接'
    )
    modified_time = models.DateTimeField(default=datetime.now, editable=False, verbose_name='最后修改时间')
    downloadable = models.BooleanField(default=False, verbose_name='是否可下载')
    official_website = models.URLField(max_length=100, blank=True, null=True, verbose_name='软件官网')
    app_size = models.FloatField(max_length=20, blank=True, null=True, verbose_name='应用大小')
    size_unit = models.CharField(max_length=4, blank=True, null=True, choices=UNIT_CHOICES, verbose_name='单位')
    app_version = models.CharField(max_length=20, blank=True, null=True, verbose_name='应用版本')
    official_download = models.URLField(max_length=200, blank=True, null=True, verbose_name='官方下载地址')
    baidu_download = models.URLField(max_length=200, blank=True, null=True, verbose_name='百度网盘下载地址')
    baidu_password = models.CharField(max_length=20, blank=True, null=True, verbose_name='百度网盘密码')
    others_download_1 = models.URLField(max_length=200, blank=True, null=True, verbose_name='其他下载地址1')
    others_download_2 = models.URLField(max_length=200, blank=True, null=True, verbose_name='其他下载地址2')
    system_requirement = models.ManyToManyField(SystemRequirement, blank=True, verbose_name='系统要求')
    category = models.ForeignKey(
        Category,
        default=get_default_category,
        on_delete=models.SET_DEFAULT,
        verbose_name='分类'
    )
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    author = models.ForeignKey(
        User,
        default=get_default_user,
        on_delete=models.SET_DEFAULT,
        verbose_name='作者'
    )

    class Meta:
        verbose_name = '所有文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_tags(self):
        return ','.join([t.name for t in self.tag.all()])

    get_tags.short_description = '标签'

    def get_tag_posts(self):
        return Post.objects.filter(tag__in=self.tag.all()).exclude(short_title=self.short_title).distinct().order_by(
            'views')[:6]

    @staticmethod
    def get_hot_posts():
        return Post.objects.all().order_by('-views')[:6]

    @staticmethod
    def get_banner_posts():
        return Post.objects.filter(is_banner=True).order_by('-views')[:4]
