from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from article.models import Post


class ArticleViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

    def test_unauthenticated_user_cannot_access_create_post(self):
        """測試未登入使用者存取發文頁面會被重定向至登入頁"""
        response = self.client.get(reverse('article:create_post'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_user_can_create_markdown_post(self):
        """測試已登入使用者可成功發表 Markdown 文章"""
        # 進行登入
        login_success = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login_success)

        # 提交文章
        post_data = {
            'title': '單元測試 Markdown 文章',
            'slug': '',  # 測試自動生成 slug
            'content': '# 測試標題\n這是一段 **粗體** 內文與 [連結](https://example.com)'
        }
        response = self.client.post(reverse('article:create_post'), post_data)
        
        # 發表成功應重定向至首頁
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # 驗證資料庫中的紀錄
        post = Post.objects.get(title='單元測試 Markdown 文章')
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.slug)  # slug 不為空
        self.assertIn('# 測試標題', post.content)

    def test_homepage_renders_markdown_as_html(self):
        """測試首頁可正確將 Markdown 字串轉譯為 HTML 渲染"""
        # 建立測試文章
        Post.objects.create(
            author=self.user,
            title='渲染測試文章',
            slug='render-test-post',
            content='## 二級標題\n\n* 列表項目 1\n* 列表項目 2'
        )

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
        # 驗證 Markdown 是否已被轉譯為 HTML 標籤
        self.assertContains(response, '二級標題')
        self.assertContains(response, '<li>列表項目 1</li>')
