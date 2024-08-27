from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to='post_files/', blank=True, null=True)

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'

    def clean(self):
        if self.file:
            file_extension = self.file.name.split('.')[-1].lower()
            if file_extension not in ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov']:
                raise ValidationError('File type is not supported. Upload an image or video file.')
    
    class Meta:
        ordering = ['-created_at']



class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Like by {self.user.username} on {self.post.id}'
