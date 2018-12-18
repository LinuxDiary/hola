from django.contrib import admin
from .models import Category, Post, Tag, SystemRequirement


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
            'title', ('excerpt', 'short_title'), 'content', ('tag', 'category', 'author', 'views', 'likes'), 'image',
            'is_banner')
        }),
        ('下载信息', {
            'classes': ('collapse',),
            'fields': (
                'downloadable', ('official_website', 'system_requirement'), ('app_size', 'size_unit'), 'app_version',
                'official_download',
                ('baidu_download', 'baidu_password'), ('others_download_1', 'others_download_2')
            )
        })
    )
    list_display = ('title', 'category', 'is_banner', 'get_tags', 'modified_time', 'create_time')
    list_editable = ('category', 'is_banner')
    list_filter = ('category', 'tag')
    search_fields = ('title', 'category', 'tag')
    ordering = ('-create_time',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_cate', 'create_time', 'get_category_posts_counts')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time')


@admin.register(SystemRequirement)
class SystemRequirementAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time')
