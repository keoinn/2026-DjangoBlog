from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from datetime import datetime

from article.models import Post
from article.forms import PostForm


def index(request):
    now = datetime.now()
    posts = Post.objects.all()
    return render(request, "index.html", {'posts': posts, 'now': now})


@login_required(login_url='/accounts/login/')
def create_post(request):
    """
    張貼文章視圖（僅限已登入使用者）
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "文章已成功發布！")
            return redirect('/')
    else:
        form = PostForm()

    return render(request, 'article/create.html', {'form': form})


def user_login(request):
    """
    使用者登入視圖
    """
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"歡迎回來，{user.username}！")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, "帳號或密碼不正確，請重新輸入。")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    """
    使用者登出視圖
    """
    logout(request)
    messages.info(request, "您已成功登出。")
    return redirect('/')