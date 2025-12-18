from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

def home(request):
    query = request.GET.get('q')
    articles = Article.objects.all().order_by('-created_at')

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    paginator = Paginator(articles, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'news/home.html', {'page_obj': page_obj})


def detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = Comment.objects.filter(article=article)

    if request.method == 'POST' and request.user.is_authenticated:
        Comment.objects.create(
            article=article,
            user=request.user,
            text=request.POST['comment']
        )
        return redirect('detail', id=id)

    return render(request, 'news/detail.html', {
        'article': article,
        'comments': comments
    })


def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'news/register.html', {'form': form})
