from django.shortcuts import render
from .models import Post,Category
from django.views.generic import ListView, DetailView


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'


    def get_context_data(self, **kargs):

        context = super(PostList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

    # 템플릿은 모델명_list.html :  post_list.html
    # 매개변수 모델명_list : post_list


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count() # 특정 조건인 레코드만 필터리
        return context

    # 템플릿은 모델명_detail.html : post_detail.html
    # 매개변수 모델명 : post


# def index(request):
    # posts = Post.objects.all().order_by('-pk')
    # return render(request, 'blog/index.html', {'posts': posts})


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog/single_post_page.html', {'post': post})

def category_page(request,slug):
    category = Category.objects.get(slug=slug)

    if slug == 'no_category':
        category='미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category=Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(request,'blog/post_list.html',{
        'post_list' : post_list,
        'categories': Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count(),
        'category' : category,
    })