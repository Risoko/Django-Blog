from django.test import TestCase
from django.utils.timezone import now, timedelta

from blog_auth.forms import SignInForm
from blog_auth.models import User

from django.contrib.auth.hashers import check_password

class TestSignInForm(TestCase):
    """
    I use primary form. I only test "confirm_login_allowed" method because 
    I override this method
    """

    def setUp(self):
        self.user = self._create_user()
        self.login_data = {
            'username': self.user.username,
            'password': 'tester123'
        }

    def _create_user(self):
        return User.objects.create_user(
            username='tester',
            email='przemyslaww.rozyckii@gmail.com',
            password='tester123',
            nick='testowy',
        )

    def test_with_banned_user(self):
        self.user.ban_user(minutes=2)
        form = SignInForm(data=self.login_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(self.user.is_ban)
        self.assertEqual(
            form.errors['__all__'][0],
            f"User about this username: {self.login_data['username']} is banned. Unlocking your account will: {self.user.end_ban}"
        )

    def test_with_end_banned_user(self):
        self.test_with_banned_user()
        self.user.end_ban = now() - timedelta(days=3)
        self.user.save()
        form = SignInForm(data=self.login_data)
        self.assertTrue(form.is_valid())