from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import CommentForm


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)  # список коментів до цього посту
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)  # отримуємо новий комент
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  # створить об'єкт коменту, але без збереження в базу
            new_comment.post = post  # приєднання Post до Коменту
            new_comment.save()  # збереження коменту в базу
    else:
        comment_form = CommentForm()  # створить інстанс форми, якщо сторінка запрошена через GET
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    if request.mothod == 'POST':
        form = EmailPostForm(request.POST)  # інстранс від форми оголошеної в forms.py
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()  # якщо не POST, а GET по просто показати форму
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})
