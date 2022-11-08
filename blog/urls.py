from django.urls import path
from . import views


urlpatterns = [  # IP주소/blog/

    path('category/<str:slug>/',views.category_page),
    path('', views.PostList.as_view()),
    path('create_post/',views.PostCreate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()), # IP주소/blog/category/slug/
    path('tag/<str:slug>/',views.tag_page),# IP주소/blog/tag/slug



]
