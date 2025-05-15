from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from blog.models import Post, Category


def sort_post(request):
    Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')
    return request


def index(request, sort_post):
    template = 'blog/index.html'
    sort_post()[:settings.MY_CONST_POSTS]

    context = {'post_list': sort_post}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        sort_post,
        id=post_id,
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug, sort_post):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    context = {
        'sort_post': sort_post(),
        'category': category,
    }
    return render(request, template, context)
