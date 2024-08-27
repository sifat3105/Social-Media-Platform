from django.shortcuts import render
from django.contrib.auth.models import User
from posts.models import Post

# Create your views here.


def home_view(request):
    posts = Post.objects.all()
    return render(request, 'home/home.html', {'posts':posts})
    