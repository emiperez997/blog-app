from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm


# Create your views here.

def home(request):
    # Posts limit to 5 ordering by date_posted
    posts = Post.objects.order_by('-date_posted')[:5]
    context = {
        'posts': posts,
        'title': 'Home',
        'page': 'home',
        'postTitle': 'Latest Posts'
    }
    return render(request, 'blog/home.html', context)


@login_required
def posts(request):
    context = {
        'posts': Post.objects.order_by('-date_posted'),
        'title': 'Posts',
        'page': 'posts',
        'postTitle': 'All Posts'
    }
    return render(request, 'blog/posts.html', context)


def about(request):
    context = {
        'title': 'About',
        'page': 'about'
    }
    return render(request, 'blog/about.html', context)


@login_required
def create_post(request):
    if request.method == 'GET':
        context = {
            'form': PostForm()
        }
        return render(request, 'blog/post_form.html', context)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog-home')
        else:
            messages.error(request, 'Error creating post!')
            return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_detail(request, id):
    if request.method == 'GET':
        post = Post.objects.filter(id=id).first()
        comments = Comment.objects.filter(post=post).order_by('-date_posted')
        context = {
            'title': post.title,
            'post': post,
            'page': 'posts',
            'postTitle': post.title,
            'form': CommentForm(),
            'comments': comments,
        }
        return render(request, 'components/post.html', context)
    elif request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = Post.objects.filter(id=id).first()
            form.save()
            messages.success(request, 'Comment created successfully!')
            return redirect('post-detail', id=id)
        else:
            messages.error(request, 'Error creating comment!')
            return redirect('post-detail', id=id)


@login_required
def update_post(request, id):
    post = Post.objects.filter(id=id).first()
    if request.method == 'GET':
        form = PostForm(instance=post)
        context = {
            'form': form,
            'title': 'Update Post',
            'id': id,
        }
        return render(request, 'blog/post_form.html', context)
    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post-detail', id=id)
        else:
            messages.error(request, 'Error updating post!')
            return render(request, 'blog/post_form.html', {'form': form})


def delete_post(request, id):
    post = Post.objects.filter(id=id).first()
    if request.method == 'GET':
        context = {
            'post': post,
            'title': 'Delete Post',
            'id': id,
        }
        return render(request, 'blog/delete_post.html', context)
    elif request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('blog-home')
