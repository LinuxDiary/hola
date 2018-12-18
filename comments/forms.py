from django import forms

from .models import Comments


class CommentsForm(forms.Form):
    author = forms.CharField(required=True, error_messages={'required': '请输入您的名字'})
    email = forms.EmailField(required=False)
    content = forms.CharField(required=True, error_messages={'required': '输入点什么吧'})
