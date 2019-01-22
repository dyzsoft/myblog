from django import template
from blog.models import Post, Category, Tag
import random

register = template.Library()


@register.simple_tag
def get_recent_post(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def get_category():
    return Category.objects.all()


@register.simple_tag
def get_post_tags(num=10):
    return Tag.objects.all()[:num]


@register.simple_tag
def random_tag_color():
    tag_colors = ["default", "primary", "success", "info", "warning",]
    return 'label-' + random.choice(tag_colors)
