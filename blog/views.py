from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from .models import Post, Category, Comment
import markdown
from django.http import Http404
from .forms import CommentForm
from django.urls import reverse_lazy


# Create your views here.


def index(request):
    post_list = Post.objects.all().order_by('-create_time')

    for post in post_list:
        post.content = markdown.markdown(post.content,
                                         extensions=[
                                             'markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc',
                                         ])

    return render(request, 'blog/index.html', context={
        'post_list': post_list
    })


class PostByCategoryListView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        post_list = category.post_set.all().order_by('-create_time')
        for post in post_list:
            post.content = markdown.markdown(post.content,
                                             extensions=[
                                                 'markdown.extensions.extra',
                                                 'markdown.extensions.codehilite',
                                                 'markdown.extensions.toc',
                                             ])

        return post_list


class PostDetailView(generic.DetailView):
    model = Post

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentForm(),
            'comment_list': self.object.comment_set.all().order_by('-create_time')
        })
        return context


class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def get_success_url(self):
        return reverse_lazy('blog:post-detail', args=[self.kwargs.get('pk')])

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
