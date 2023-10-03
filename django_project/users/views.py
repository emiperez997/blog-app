from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.


def login_blog(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in!')
            return redirect('blog-home')

        form = LoginForm()
        context = {
            'form': form,
            'title': 'Login',
        }
        return render(request, 'users/login.html', context)

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(
                request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Login successful!')

                return redirect('blog-home')
            else:
                messages.error(request, 'Invalid username or password!')
                return render(request, 'users/login.html', {'form': form})
        else:
            return render(request, 'users/login.html', {'form': form})


@login_required
def logout_blog(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')


def register_blog(request):
    if request.method == 'GET':
        form = RegisterForm()
        context = {
            'form': form,
            'title': 'Register',
        }

        return render(request, 'users/register.html', context)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    user = User.objects.filter(id=request.user.id).first()
    user_posts = Post.objects.filter(author=user).order_by('-date_posted')
    context = {
        'title': 'Profile',
        'page': 'profile',
        'user': user,
        'posts': user_posts,
        'postTitle': f"{user.username}'s Posts",
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'GET':
        form = RegisterForm(instance=request.user)
        context = {
            'title': 'Edit Profile',
            'form': form,
            'id': request.user.id,
        }
        return render(request, 'users/register.html', context)

    elif request.method == 'POST':
        form = RegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating profile!')
            return render(request, 'users/register.html', {'form': form})


@login_required
def user_posts(request, username):
    user = User.objects.filter(username=username).first()

    if not user:
        messages.error(request, 'User not found!')
        return redirect('blog-home')

    user_posts = Post.objects.filter(author=user).order_by('-date_posted')
    context = {
        'title': f"{user.username}'s Posts",
        "postTitle": f"{user.username}'s Posts",
        'page': 'my-posts',
        'user': user,
        'posts': user_posts,
    }
    return render(request, 'users/user_posts.html', context)
