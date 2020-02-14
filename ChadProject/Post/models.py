from django.db import models
from django.shortcuts import reverse

from Accounts.models import User
from uuid import uuid4


def post_directory(instance, filename):
    file_extension = filename.split('.')[-1]
    filename = f'post_{instance.id}.{file_extension}'
    return f'photos/User-{instance.owner.username}/Posts/{filename}'


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    photo = models.ImageField(upload_to=post_directory)
    captions = models.TextField(max_length=420, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(
        User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f'Post [{self.id}]'

    def get_absolute_url(self):
        return reverse("Post:Detail", kwargs={"pk": self.pk})
    


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner.username} [{self.comment[:10]} . . .]'
