from django.shortcuts import render, redirect
from .models import Post,Category,Tag, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q


# Create your views here.

class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category'] # , tags 입력받은 형태로 하기 위해 tags를 지움

    # 모델명.html 특정한 템플릿을 지정해서 불러준다.
    template_name = 'blog/post_update_form.html'
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author :
            return super(PostUpdate,self).dispatch(request,*args,**kwargs)
        else:
            raise PermissionDenied


    def form_valid(self,form):
        response = super(PostUpdate,self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()  # 빈칸을 없애주는 명령어
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)  # 주어진 태그를 네임으로 하는 데 있으면 create, 없으면 get 한다.
                if is_tag_created:  # 기존 태그 모델이 있을 경우
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


    def get_context_data(self, *, object_list=None,**kwargs):

        context = super(PostUpdate,self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list() # 빈 리스트를 하나 만든다.
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] =';'.join(tags_str_list) # 포스트 연결에 되어있는 태그 모델들을 배열로 만드는 작업 필요

        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image','file_upload','category'] # 태그 입력 가능하게 변경 함 (tags 추가 안함 )
    #모델명_form.html

    # 이벤트가 발생했을 자동적으로 해당 함수 호출 -->

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
        # superuser냐 아니면 is_staff냐



    def form_valid(self,form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser): #올바르게 인증된 유저일경우에만
            form.instance.author = current_user

            response = super(PostCreate,self).form_valid(form)
            tags_str = self.request.POST.get('tags_str') # POST 는 모델을 의미하는 게 아니라
            # get 방식과 post 방식을 이용한 방식 (웹 동작에서 )

            if tags_str:
                tags_str = tags_str.strip() # 빈칸을 없애주는 명령어
                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t) # 주어진 태그를 네임으로 하는 데 있으면 create, 없으면 get 한다.
                    if is_tag_created: # 기존 태그 모델이 있을 경우
                        tag.slug = slugify(t,allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
        else:
            return redirect('/blog/') # 다시 url을 전달해서 목록 페이지를 전달하겠다.

    def get_context_data(self, *, object_list=None,**kwargs):

        context = super(PostCreate,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context



class PostList(ListView):
    model = Post
    ordering = '-pk'

    paginate_by = 5 # 구분 해서 보여줄꺼야

    def get_context_data(self, *, object_list=None,**kwargs): # 추가인자

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
        context['comment_form'] = CommentForm
        return context


    # 템플릿은 모델명_detail.html : post_detail.html
    # 매개변수 모델명 : post


# def index(request):
    # posts = Post.objects.all().order_by('-pk')
    # return render(request, 'blog/index.html', {'posts': posts})


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog/single_post_page.html', {'post': post})

def new_comment(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,pk=pk) # POST를 가져온다.

        if request.method == 'POST': # submit 버튼을 클릭하면 POST 방식으로 전달이 된다.
            comment_form = CommentForm(request.POST)
            if request.method == 'POST':
                comment_form = CommentForm(request.POST) # POST 방식으로 서버에 요청이 들어왔다면
                # POST 방식으로 들어온 정보를 CommentForm의 형태로 가져온다.
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.post = post
                    comment.author = request.user
                    comment.save() # commnet라는 객체는 서버에 있는 모델에 저장이 된다.
                    return redirect(post.get_absolute_url())
        else: #GET으로 들어왔다면
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

class PostSearch(PostList): # ListView 상속, post_list, post_list.html  자동으로 연결
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title_contains = q) | Q(tags__name__contains=q)

        ).distinct() # 중복으로 가져온 요소가 있을 때 한 번만 나타나게 하기 위한 설정
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search:{q} ({self.get_queryset().count()})'

        return context



class CommentUpdate(LoginRequiredMixin, UpdateView):

    # comment_form
    model = Comment
    form_class = CommentForm # commenform에 필드명이 들어가 있다.

    # 쳄플릿 : comment_form


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate,self).dispatch(request,*args,**kwargs)
        else:
            return PermissionDenied

# FBV로 작성하기

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

def tag_page(request,slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all
    return render(request, 'blog/post_list.html', {
        'tag': tag,
        'post_list':post_list,
        'categories' : Category.objects.all(),
        'no_category_post_count':Post.objects.filter(category=None).count(),
    })

