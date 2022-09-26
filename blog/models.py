from django.db import models
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    # 추후 author 작성

    def __str__(self):
        return f'[{self.pk}]{self.title}   {self.created_at}'
