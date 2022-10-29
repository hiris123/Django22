from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 50, unique = True) # 동일한 name을 갖는 카테고리를 만들 수 있다 .
    slug = models.SlugField(max_length = 200, unique = True, allow_unicode = True) # 사람이 읽을 수 있는 텍스트로 고유 URL
    # slug는 name에 대한 url 값이다

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    # Meta로 모델의 복수형 알려주기
    class Meta:
        verbose_name_plural = 'categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)

    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # 추후 author 작성 user table에 등록되어 있는 것을 가져옴 ( 이 포스트의 작성자가 데이터베이스에서 삭제되었을 때
    # 작성자명을 빈 칸으로 둔다'
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # ' 이 포스트의 작성자가 데이터베이스에서 삭제되었을 때 이 포스트도 같이 삭제한다.'
    # author = models.ForeignKey(User, on_delete=models.CASCADE)


    # Post 모델에 category 필드 추가하기 ( 관리자 페이지에서 카테고리를 빈 칸으로 지정할 수 있게 된다. )
    category = models.ForeignKey(Category,null=True, blank=True, on_delete=models.SET_NULL)


    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author} : {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  # a.b.text => a b text
