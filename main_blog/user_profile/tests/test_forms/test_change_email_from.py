from django.test import TestCase
from django.contrib.auth.hashers import check_password

from blog_auth.forms import SignUpForm
from blog_auth.models import User
from user_profile.forms import ChangeEmailForm

class TestChangeEmailFrom(TestCase):
    
    def setUp(self):
        self.user_data = {
            'username' : 'tester',
            'nick' : 'testowy',
            'password1' : 'test123456',
            'password2' : 'test123456',
            'email' : 'przemyslaw.rozycki@smcebi.edu.pl',
        }
        self.change_email_data = {
            'new_adress_email1' : 'przemyslaww.rozyckii@gmail.com',
            'new_adress_email2' : 'przemyslaww.rozyckii@gmail.com'
        }
        form = SignUpForm(data=self.user_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user = User.objects.get(username=self.user_data['username'])

    def test_change_email_with_correct_data(self):
        form = ChangeEmailForm(user=self.user, data=self.change_email_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(self.user.email == self.change_email_data['new_adress_email2'])
        self.assertFalse(self.user.email == self.user_data['email'])

    def test_change_email_with_empty_new_adress_email1(self):
        del self.change_email_data['new_adress_email1']
        form = ChangeEmailForm(user=self.user, data=self.change_email_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_adress_email1'][0], "This field is required.")
        self.assertFalse(self.user.email == self.change_email_data['new_adress_email2'])
        self.assertTrue(self.user.email == self.user_data['email'])

    def test_change_email_with_empty_new_adress_email2(self):
        del self.change_email_data['new_adress_email2']
        form = ChangeEmailForm(user=self.user, data=self.change_email_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_adress_email2'][0], "This field is required.")
        self.assertFalse(self.user.email == self.change_email_data['new_adress_email1'])
        self.assertTrue(self.user.email == self.user_data['email'])

    def test_change_password_with_mismatched_email(self):
        self.change_email_data['new_adress_email2'] = 'mismatch_email@gmail.com'
        form = ChangeEmailForm(user=self.user, data=self.change_email_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_adress_email2'][0], "The two email fields didn't match.")
        self.assertFalse(self.user.email == self.change_email_data['new_adress_email2'])
        self.assertTrue(self.user.email == self.user_data['email'])

    def test_change_password_with_incorrect_email(self):
        self.change_email_data['new_adress_email2'] = 'incorrect_email'
        form = ChangeEmailForm(user=self.user, data=self.change_email_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_adress_email2'][0], "Enter a valid email address.")
        self.assertFalse(self.user.email == self.change_email_data['new_adress_email2'])
        self.assertTrue(self.user.email == self.user_data['email'])
