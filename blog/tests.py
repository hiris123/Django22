from django.test import TestCase, Client

from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User
# Create your tests here.

# python manage.py test blog.tests.TestView.test_post_list
class TestView(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_kim = User.objects.create_user(username="kim",password="somepassword")
        self.user_lee = User.objects.create_user(username="lee", password="somepassword")

        # 데이터베이스에 카테고리가 2개 생성되어 있는 상태로 만들 수 있다.
        self.category_com = Category.objects.create(name="computer",slug="computer")
        self.category_edu = Category.objects.create(name="education", slug="education")

        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.",
                                            author=self.user_kim, category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.",
                                            author=self.user_lee, category=self.category_edu)
        self.post_003 = Post.objects.create(title="세번째 포스트", content="세번째 포스트입니다.",
                                            author=self.user_lee)
    def nav_test(self,soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # a 요소를 찾아 logo_btn 변수에 담는다.
        home_btn = navbar.find('a',text="Home")
        # a 요소에서 href 속성을 찾아 값이 '/'인지 확인한다.
        self.assertEqual(home_btn.attrs['href'],'/')


        blog_btn = navbar.find('a',text="Blog")
        self.assertEqual(blog_btn.attrs['href'],'/blog/')

        about_btn = navbar.find('a', text="About Me")
        self.assertEqual(about_btn.attrs['href'], '/about_me/')



    def category_test(self, soup):
        category_card = soup.find('div',id="category_card")
        self.assertIn('Categories', category_card.text)
        self.assertIn(f'{self.category_com.name} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_edu.name} ({self.category_edu.post_set.count()})', category_card.text)
        #self.assertIn(f'미분류 ({self.category_edu.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text)

    def test_post_list(self):

        # 포스가 있는 경우
        self.assertEqual(Post.objects.count(),3)
        # 301 오류가 날 경우에는 follow = True 의 코드를 추가한다.
        response = self.client.get('/blog/')

        # response  결과가 정상적으로 보이는 지
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')  # html 내용 응답
        # title이 정상적으로 보이는 지
        self.assertEqual(soup.title.text, 'Blog')

        # navbar가 정상적으로 보이는 지 ,category_test가 정상적으로 보이는지
        self.nav_test(soup)
        self.category_test(soup)

        main_area = soup.find('div', id="main-area")
        self.assertNotIn('아직 게시물이 없습니다',main_area.text)


        response = self.client.get('/blog/', follow=True)

        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")

        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)


        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)

        #post가 정상적으로 보이는지
        # 포스트가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response=self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')  # html 내용 응답

        main_area = soup.find('div', id="main-area")
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 2. Post가 추가

        # post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.",
        #                                author = self.user_kim)
        # post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다. ",
        #                                author=self.user_lee)



    def test_post_detail(self):
        post_001= Post.objects.create(title="첫번째 포스트", content="첫번째 포스트 입니다.",
                                       author=self.user_kim)
        self.assertEqual(post_001.get_absolute_url(), '/blog/4/')

        response = self.client.get(
            post_001.get_absolute_url(),  follow=True)  # '/blog/1'
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # navbar 가 정상적으로 보이는 지
        self.nav_test(soup)

        # 첫번재 포스트 제목이 포스트 영역 (post area)에 있다.
        main_area = soup.find('div', id="main-area")
        post_area = main_area.find('div', id="post-area")


        self.assertIn(post_001.title,   post_area.text)
        self.assertIn(post_001.title, soup.title.text)
        self.assertIn(post_001.content, post_area.text)
        self.assertIn(post_001.author.username.upper(), post_area.text)

        # title에 대한 포스트에 있나
        self.assertIn(post_001.title, soup.title.text)

