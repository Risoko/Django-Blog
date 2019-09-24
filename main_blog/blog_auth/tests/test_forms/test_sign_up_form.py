from datetime import date

from django.test import TestCase
from django.contrib.auth.hashers import check_password

from blog_auth.forms import SignUpForm
from blog_auth.models import User

class TestSignUpForm(TestCase):

    def setUp(self):
        self.registr_data = {
            'username': 'tester',
            'nick': 'test',
            'email': 'przemyslaww.rozyckii@gmail.com',
            'password1' : 'test123456',
            'password2' : 'test123456',
        }

    def test_with_correct_data(self):
        form = SignUpForm(data=self.registr_data)
        self.assertTrue(form.is_valid())
        form.save()
        user = User.objects.get(username=self.registr_data['username'])
        self.assertEqual(user.username, self.registr_data['username'])
        self.assertEqual(user.nick, self.registr_data['nick'])
        self.assertEqual(user.email, self.registr_data['email'])
        self.assertTrue(check_password(password=self.registr_data['password1'], encoded=user.password))

    def test_with_empty_username_field(self):
        del self.registr_data['username']
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'][0], "This field is required.")

    def test_with_username_that_contains_inappropriate_characters(self):
        self.registr_data['username'] = 'Uwq!#'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'][0],
            "Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."
        )
 
    def test_with_exist_username_in_database(self):
        self._create_form()
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'][0],
            "A user with that username already exists."
        )

    def test_with_username_too_long(self):
        self.registr_data['username'] = 100 * 'UaWr'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'][0],
            "Ensure this value has at most 150 characters (it has 400)."
        )

    def test_username_with_only_digit(self):
        self.registr_data['username'] = '12345'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'][0],
            "Username can't be only digit."
        )

    def test_with_same_username_and_nick(self):
        self.registr_data['username'] = self.registr_data['nick']
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['__all__'][0],
            "Nick and username can't be same test != test"
        )

    def test_with_empty_nick_field(self):
        self.registr_data['nick'] = ''
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['nick'][0], "This field is required.")

    def test_with_nick_that_contains_inappropriate_characters(self):
        self.registr_data['nick'] = 'U#'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['nick'][0],
            "Nick must be only alphanumeric."
        )
 
    def test_with_exist_nick_in_database(self):
        self._create_form()
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['nick'][0],
            "A user with that nick already exists."
        )

    def test_with_nick_too_long(self):
        self.registr_data['nick'] = 100 * 'UaWr'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['nick'][0],
            "Ensure this value has at most 20 characters (it has 400)."
        )
    
    def test_with_nick_too_short(self):
        self.registr_data['nick'] = 'UaW'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['nick'][0],
            "Ensure this value has at least 4 characters (it has 3)."
        )

    def test_nick_with_only_digit(self):
        self.registr_data['nick'] = '12345'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['nick'][0],
            "Nick can't be only digit."
        )

    def test_with_empty_email_field(self):
        del self.registr_data['email'] 
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], "This field is required.")

    def test_with_email_that_contains_inappropriate_characters(self):
        self.registr_data['email'] = 'U#'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'][0],
            "Enter a valid email address."
        )
 
    def test_with_exist_email_in_database(self):
        self._create_form()
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'][0],
            "A user with that email already exists."
        )

    def test_with_email_too_long(self):
        self.registr_data['email'] = 10 * self.registr_data['email']
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'][0],
            "Enter a valid email address."
        )
    
    def test_email_with_only_digit(self):
        self.registr_data['email'] = '12345'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'][0],
            "Enter a valid email address."
        )

    def test_with_empty_password_field(self):
        del self.registr_data['password1']
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password1'][0], "This field is required.")

    def test_with_password_too_short(self):
        self.registr_data['password1'] = 'asasa'
        self.registr_data['password2'] = 'asasa'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password2'][0],
            "This password is too short. It must contain at least 8 characters."
        )

    def test_password_with_only_digit(self):
        self.registr_data['password1'] = '123456789'
        self.registr_data['password2'] = '123456789'
        form = SignUpForm(data=self.registr_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password2'][0],
            "This password is too common."
        )

    def _create_form(self):
        form = SignUpForm(data=self.registr_data)
        self.assertTrue(form.is_valid())
        form.save()









