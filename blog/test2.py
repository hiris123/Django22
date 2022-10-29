
from django.test import TestCase, Client

from bs4 import BeautifulSoup
from .models import Post
from django.contrib.auth.models import User

### 명령어 python manage.py test2 blog.test2.TestView.test_post_list

class TestView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_kim = User.objects.create_user(username="kim",password="somepassword")
        self.user_lee = User.objects.create_user(username="lee", password="somepassword")
    def test_post_list(self):
        # 301 오류가 날 경우에는 follow = True 의 코드를 추가한다.
        response = self.client.get('/blog/')

        # response  결과가 정상적으로 보이는 지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')  # html 내용 응답
        # title이 정상적으로 보이는 지
        self.assertEqual(soup.title.text, 'Blog')

        # navbar가 정상적으로 보이는 지
        # 타이틀 안에 있는 글자와 같을 때는 assertIn
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', soup.nav.text)

        # post가 정상적으로 보이는 지
        # 1. 맨 처음엔 Post가 없음

        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id="main-area")
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 2. Post가 2개 있다면
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.",
                                       author = self.user_kim)
        post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다. ",
                                       author=self.user_lee)
        self.assertEqual(Post.objects.count(), 2)

        # 포스트 목록 페이지를 새로고침했을 때
        response = self.client.get('/blog/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        #main area에 포스트 2개의 제목이 존재한다.
        main_area = soup.find('div', id="main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 아직 게시물이 없습니다 라는 문구는 더 이상 나타나지 않는다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        self.assertIn(post_001.author.username.upper(),main_area.text)
        self.assertIn(post_002.author.username.upper(), main_area.text)

    def test_post_detail(self):
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.",
                                       author=self.user_kim)
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(
            post_001.get_absolute_url(), follow=True)  # '/blog/1'
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # navbar 가 정상적으로 보이는 지
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', soup.nav.text)

        # 첫번재 포스트 제목이 포스트 영역 (post area)에 있다.
        main_area = soup.find('div', id="main-area")
        post_area = main_area.find('div', id="post-area")

        #첫번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(post_001.title, soup.title.text)
        self.assertIn(post_001.content, post_area.text)
        self.assertIn(post_001.author.username.upper(), post_area.text)


        # title에 대한 포스트에 있나
        self.assertIn(post_001.title, soup.title.text)
