# django 博客系统
> django 练习使用

## markdown的使用
```python
import markdown

post.content = markdown.markdown(post.content,
             extensions=[
                 'markdown.extensions.extra',
                 'markdown.extensions.codehilite',
                 'markdown.extensions.toc',
             ])
```
pygmentize 的使用 生成 css文件，可以使得 markdown中的代码 片段高亮 

`pygmentize -f html -a .highlight -S default > pygments.css`

## 增加评论注意事项

 `path('post/<int:pk>/comment/create', views.CommentCreateView.as_view(), name="post-comment-create"),`
 
1. 增加CreateView
    ```python
    class CommentCreateView(generic.CreateView):
           model = Comment
           form_class = CommentForm
           template_name = 'blog/post_detail.html'
    ```
    由于和pagedetail 共用的一个模板，所以需要在 CommentCreateView的contenxt中，增加该模板上用到的所有context变量
    ```python
        def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get(self.pk_url_kwarg))
        context = super().get_context_data(**kwargs)
        """
            由于 使用的是  blog/post_detail.html 这个模板，所以，需要将该模板用到的所有content都赋值才行。
            否则 模板 在解析的过程中找不到对应的变量，会报错。
        """
        context.update({
            'post': post,
            'comment_list': post.comment_set.all().order_by('-create_time')
        })
        return context
    ```
2. 在CreateView 中可以获取当前的文章  
    通过 `self.kwargs.get(self.pk_url_kwarg))` 可以获取文章的主键，然后可以获取post对象
    