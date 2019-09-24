from django.test import TestCase

from blog_auth.models import User
from blog_entries.models import Article
from blog_entries.forms import CreateArticleForm

class TestCreateArticleForm(TestCase):
    
    def setUp(self):
        self.user = self._create_user()
        self.article_data = {
            'title': 'Tester title',
            'entry': 20 * 'I am tester. My job is very difficult'
        }

    def _create_user(self):
        return User.objects.create_user(
            username='tester',
            email='przemyslaww.rozyckii@gmail.com',
            password='tester123',
            nick='testowy',
        )

    def test_with_correct_data(self):
        form = CreateArticleForm(user=self.user, data=self.article_data)
        self.assertTrue(form.is_valid())
        form.save()
        article = Article.objects.get(title=self.article_data['title'])
        self.assertEqual(article.title, self.article_data['title'])
        self.assertEqual(article.entry, self.article_data['entry'])
        self.assertEqual(article.author.username, self.user.username)
        self.assertEqual(article.author.nick, self.user.nick)

    def test_with_empty_title(self):
        del self.article_data['title']
        form = CreateArticleForm(user=self.user, data=self.article_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['title'][0], 
            "This field is required."
        )

    def test_with_too_short_title(self):
        self.article_data['title'] = 'Test'
        form = CreateArticleForm(user=self.user, data=self.article_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['title'][0],
            "Ensure this value has at least 10 characters (it has 4)."
        )

    def test_with_too_long_title(self):
        self.article_data['title'] = 100 * 'Test'
        form = CreateArticleForm(user=self.user, data=self.article_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['title'][0],
            "Ensure this value has at most 300 characters (it has 400)."
        )

    def test_with_only_digits_in_title(self):
        self.article_data['title'] = 3 * '1121111'
        form = CreateArticleForm(user=self.user, data=self.article_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['title'][0],
            "You can't use only digit."
        )

    def test_with_empty_entry(self):
        del self.article_data['entry']
        form = CreateArticleForm(user=self.user, data=self.article_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['entry'][0], 
            "This field is required."
        )

    def test_with_too_short_entry(self):
        self.article_data['entry'] = 'Test'
        form = CreateArticleForm(user=self.user, data=self.article_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['entry'][0],
            "Ensure this value has at least 200 characters (it has 4)."
        )

    def test_with_only_digits_in_entry(self):
        self.article_data['entry'] = 20 * '1120909096867'
        form = CreateArticleForm(user=self.user, data=self.article_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['entry'][0],
            "You can't use only digit."
        )




