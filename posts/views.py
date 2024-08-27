from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required(login_url='/auth/login/?next=/create/post/')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        file = request.FILES.get('media')
        post = Post.objects.create(author = request.user)
        post.content = content
        post.file = file
        post.save()
        
    return redirect(request.META.get('HTTP_REFERER', '/'))
    
