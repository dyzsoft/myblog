from django.contrib import admin

from .models import Post, Category, Tag, Comment


# Register your models here.

class CommentAdminInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'content')
    list_display = ('title', 'create_time', 'modified_time')

    fieldsets = [
        ('文章信息', {'fields': ['title', 'summary', 'content', 'author']}),
        ('其他', {'fields': ['modified_time', 'category', 'tag']}),
    ]
    inlines = [CommentAdminInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fieldsets = [
        ('标签信息', {'fields': ['name']}),
    ]
