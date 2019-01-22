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
3. form校验完成之后(即用户输入的数据校验完成)，可以针对form关联的数据库其他字段进行填充
    ```python
         def form_valid(self, form):
            """
                name = models.CharField(max_length=255)
                content = models.TextField()
                create_time = models.DateTimeField(auto_now_add=True)
                ip_address = models.GenericIPAddressField(null=True, blank=True, default='')
                post = models.ForeignKey(Post, on_delete=models.CASCADE, )
    
                用户填写评论名称和内容，当提交的form校验完成之后，
                可以关联 ip 地址信息，  ip地址信息是系统通过request字段自动获取上来的
                同时关联上post信息，然后调用super方法，进行comment的保存。
    
            :param form:
            :return:
            """
            post = get_object_or_404(Post, pk=self.kwargs.get(self.pk_url_kwarg))
            form.instance.post = post
            form.instance.ip_address = self.request.META['REMOTE_ADDR']
            return super().form_valid(form)
    ```
    `form.instance` 即为form关联的数据库对象
4. 在view相关的类中，可以使用 get_object方法，对object进行改写,例如：
    将 文章的 markdown内容转变为 html内容：
    ```python
        def get_object(self, queryset=None):
            """
                如果用户恶意请求，父类找不到会raise Http404
                这里不需要进行检查。
                获取对象后，对对象的content内容进行 marddown 到 html的编码。
            :param queryset:
            :return:
            """
            post = super().get_object(queryset=None)
            post.content = markdown.markdown(post.content,
                                             extensions=[
                                                 'markdown.extensions.extra',
                                                 'markdown.extensions.codehilite',
                                                 'markdown.extensions.toc',
                                             ])
            return post
    ```
5. 如何自定义标签：
   需要在app文件夹中，新建templatetags 文件夹，建立__init__.py 同时，增加xxx_tags.py文件，在该文件中增加既可。
   
    ```python
       from django import template
       from blog.models import Post, Category, Tag
       import random
        
       register = template.Library()
        
        
       @register.simple_tag
       def get_recent_post(num=5):
           return Post.objects.all().order_by('-create_time')[:num]
    ```
    使用标签时，通过 `{% load blog_tags %}` 进行标签库的加载，如果不成功，需要重启开发服务器。