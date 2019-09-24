from django.test import TestCase

from blog_auth.models import User
from blog_entries.models import Article, Comment
from blog_entries.forms import CreateCommentForm

class TestCreatecommentForm(TestCase):
    
    def setUp(self):
        self.user = self._create_user()
        self.article = self._create_article()
        self.comment_data = {
            'content_comment':  'I am tester. My job is very difficult'
        }

    def _create_user(self):
        return User.objects.create_user(
            username='tester',
            email='przemyslaww.rozyckii@gmail.com',
            password='tester123',
            nick='testowy',
        )

    def _create_article(self):
        return Article.objects.create_article(
            author=self.user,
            title='Test is very good.',
            entry= 50 * 'Test.'
        )

    def test_with_correct_data(self):
        form = CreateCommentForm(user=self.user, article=self.article, data=self.comment_data)
        self.assertTrue(form.is_valid())
        form.save()
        comment = Comment.objects.get(content_comment=self.comment_data['content_comment'])
        self.assertEqual(comment.content_comment, self.comment_data['content_comment'])
        self.assertEqual(comment.owner.username, self.user.username)
        self.assertEqual(comment.owner.nick, self.user.nick)
        self.assertEqual(comment.article.title, self.article.title)
        self.assertEqual(comment.article.entry, self.article.entry)

    def test_with_empty_comment(self):
        del self.comment_data['content_comment']
        form = CreateCommentForm(user=self.user, article=self.article, data=self.comment_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['content_comment'][0], 
            "This field is required."
        )

    def test_with_too_short_comment(self):
        self.comment_data['content_comment'] = 'Test'
        form = CreateCommentForm(user=self.user, article=self.article, data=self.comment_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['content_comment'][0],
            "Ensure this value has at least 10 characters (it has 4)."
        )

    def test_with_too_long_comment(self):
        self.comment_data['content_comment'] = 101 * 'Test'
        form = CreateCommentForm(user=self.user, article=self.article, data=self.comment_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['content_comment'][0],
            "Ensure this value has at most 400 characters (it has 404)."
        )

    def test_with_only_digits_in_comment(self):
        self.comment_data['content_comment'] = 3 * '1121111'
        form = CreateCommentForm(user=self.user, article=self.article, data=self.comment_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['content_comment'][0],
            "You can't use only digit."
        )