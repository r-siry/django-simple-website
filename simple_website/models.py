from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class MakePost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500, blank=True)
    photo = ResizedImageField(size=[500, 300], quality=100, upload_to='simple_website/images/', null=True, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
