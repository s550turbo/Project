from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUp
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import PostForm
from django.utils import timezone

# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-pub_date')
    if request.method == 'POST':
        username = request.POST['username'] 
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have sucessfully been logged in") 
            return redirect('home')
        else:
            messages.success(request, "There was an error with your login")  
            return redirect('home')
    else:
        return render(request, 'home.html', {'posts': posts})
    

def logout_user(request):
    logout(request)
    messages.success(request, "You have been sucessfully logged out")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect('home')
    else:
        form = SignUp()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form': form})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = PostForm()
        return render(request, 'add_post.html', {'form': form})
    
class PostList(ListView):
    model = Post
    template_name = 'home.html'

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'