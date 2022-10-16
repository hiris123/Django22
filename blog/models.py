from django.db import models
from django.utils import timezone
import os

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)
<<<<<<< HEAD
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
=======
    # %Y 2022, %y 22
    file_upload = models.FileField(
        upload_to='blog/files/%Y/%m/%d/', blank=True)

>>>>>>> e29d0cd0b06e226a0839689b8731669d43210c43
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 추후 author 작성

    def __str__(self):
        return f'[{self.pk}]{self.title}   {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload_name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  # a.b.text => a b text
