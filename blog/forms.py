from django import forms
from django.core.validators import ValidationError
from django.forms import widgets as wid
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content', ]
        widgets = {
            'name': wid.TextInput(attrs={'class': 'form-control'}),
            'content': wid.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': '名字',
            'content': '评论内容',
        }

    name = forms.CharField(min_length=2, error_messages={
        'required': '请填写名字',
        'min_length': '最小长度为2，长度不够',
    }, widget=wid.TextInput(attrs={'class': 'form-control'}))

    content = forms.CharField(min_length=10, error_messages={
        'required': '请填写名字',
        'min_length': '最小长度为10,请说点什么吧。。。',
    }, widget=wid.Textarea(attrs={'class': 'form-control'}))

    def clean_name(self):
        data = self.cleaned_data['name']
        if data.find('admin') != -1:
            raise ValidationError('不能使用admin提交信息')
        return data

    def clean_content(self):
        data = self.cleaned_data['content']
        if data.find('admin') != -1:
            raise ValidationError('提交的评论内容不能包含admin哦。。。')
        return data
