from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .const import LIMIT
from blog.models import Post, Category

def sort_post():
    return Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    template = 'blog/index.html'
    post_list = sort_post()[:LIMIT]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        sort_post,
        pk=id,
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Category.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )
    context = {
        'post_list': post_list,
        'category': category,
    }
    return render(request, template, context)
