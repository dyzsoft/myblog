from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name="index"),

    path('post/<int:pk>', views.PostDetailView.as_view(), name="post-detail"),
    path('category/<int:pk>', views.PostByCategoryListView.as_view(), name="category-post-list"),

    path('post/<int:pk>/comment', views.PostByCategoryListView.as_view(), name="post-comment-list"),
    # path('post/<int:pk>/comment/create', views.CommentCreateFromView.as_view(), name="post-comment-create"),
    path('post/<int:pk>/comment/create', views.CommentCreateView.as_view(), name="post-comment-create"),

    path('comment/create', views.CommentCreateView.as_view(), name="comment-create"),
]
