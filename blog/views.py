# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm


# Create your views here.

def post_list(request):
    if request.user.is_authenticated():
        posts = Post.objects.filter(author__username=request.user.username).filter(
            published_date__isnull=False).order_by('-published_date')
    else:
        posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required
def post_all(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    return render(request, 'blog/post_all.html', {'posts': posts})


def post_detail(request, pk):
    refer = request.META.get('HTTP_REFERER')
    post = get_object_or_404(Post, pk=pk)
    if post.published_date is None:
        if not request.user.is_authenticated():
            messages.warning(request, 'Not allowed to access this.')
            return redirect('post_list')
        if request.user.is_superuser or post.author.username == request.user.username:
            return render(request, 'blog/post.html', {'post': post, 'refer': refer})
        else:
            messages.warning(request, 'Not allowed to access this.')
            return redirect('post_list')
    return render(request, 'blog/post.html', {'post': post, 'refer': refer})


@login_required
def post_draft(request):
    posts = Post.objects.filter(author__username=request.user.username).filter(published_date__isnull=True).order_by(
        'created_date')
    return render(request, 'blog/drafts.html', {'posts': posts})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    error = 'edit'
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
    if request.user.is_superuser or post.author.username == request.user.username:
        form = PostForm(instance=post)
        refer = request.META.get('HTTP_REFERER')
        return render(request, 'blog/post_new.html', {'form': form, 'refer': refer, 'error': error})
    else:
        messages.warning(request, 'Not allowed to access this.')
        refer = request.META.get('HTTP_REFERER')
        return redirect('post_list')


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_superuser or post.author.username == request.user.username:
        post.publish()
        return redirect('post_detail', pk=pk)
    else:
        messages.warning(request, 'Not allowed to access this.')
        return redirect('post_list')


@login_required
def post_delete(request, pk):
    refer = request.META.get('HTTP_REFERER')
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if request.user.is_superuser or post.author.username == request.user.username:
            post.delete()
            return redirect('post_list')
        else:
            messages.warning(request, 'Not allowed to access this.')
            return redirect('post_list')
    return render(request, 'blog/post_delete.html', {'refer': refer, 'post': post})


@login_required
def post_new(request):
    refer = request.META.get('HTTP_REFERER')
    error = None
    if request.method == 'POST':
        form = PostForm(request.POST)
        if 'submit2' in request.POST:
            if form.is_valid():
                form = PostForm(request.POST)
                post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    if 'submit1' in request.POST:
        if form.is_valid():
            form = PostForm(request.POST)
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_draft')
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form, 'refer': refer, 'error': error})
