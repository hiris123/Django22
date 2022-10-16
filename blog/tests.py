from django.test import TestCase, Client

from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.


class TestView(TestCase):

    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 301 오류가 날 경우에는 follow = True 의 코드를 추가한다.
        response = self.client.get('/blog/')

        # response  결과가 정상적으로 보이는 지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
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

        # 2. Post가 추가

        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.")
        post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다. ")
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
