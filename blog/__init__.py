
#####
###venv/Scripts/activate.bat
#python manage.py startapp blog ( blog라는 앱 생성)
#[settings.py]
#'blog',
#col-sm, md, lg, xl

#########
# <div class ="row">
#         <div class="col-md-8 col-lg-9">
#         <h1>Blog</h1>
#         </div>
#         <div class="col-md-4 col-lg-3">
#         <p>작성하지 않았습니다.</p>
#         </div>
#     </div>
# #

## 포스트 상세 페이지에 부트스트랩 적용하기


# 1. 내비게이션 고정
# post_detail.html - nav class인 navbar에서 fixed-top 추가하기
#
# {% if p.head_image %}
# 		<img class ="card-img-top" src="{{p.head_image.url}}" alt="{{p}} head image">
#
# {% endif %}

