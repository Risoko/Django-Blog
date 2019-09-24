from django.test import TestCase
from django.contrib.auth.hashers import check_password

from blog_auth.forms import SignUpForm
from blog_auth.models import User
from user_profile.forms import ChangePasswordForm

class TestChangePasswordForm(TestCase):
    
    def setUp(self):
        self.user_data = {
            'username' : 'tester',
            'nick' : 'testowy',
            'password1' : 'test123456',
            'password2' : 'test123456',
            'email' : 'przemyslaw.rozycki@smcebi.edu.pl',
        }
        self.change_password_data = {
            'old_password' : self.user_data['password1'],
            'new_password1' : 'TestChangePassword',
            'new_password2' : 'TestChangePassword'
        }
        form = SignUpForm(data=self.user_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user = User.objects.get(username=self.user_data['username'])

    def test_change_password_with_correctly_data(self):
        form = ChangePasswordForm(user=self.user, data=self.change_password_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(check_password(password=self.change_password_data['new_password1'], encoded=self.user.password))
        self.assertFalse(check_password(password=self.change_password_data['old_password'], encoded=self.user.password))

    def test_change_password_with_bad_old_password(self):
        self.change_password_data['old_password'] = 'bad_password'
        form = ChangePasswordForm(user=self.user, data=self.change_password_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['old_password'][0], "Old password does not match existing password.")
        self.assertFalse(check_password(password=self.change_password_data['new_password1'], encoded=self.user.password))
        self.assertTrue(check_password(password=self.user_data['password1'], encoded=self.user.password))

    def test_change_password_with_empty_field_old_password(self):
        del self.change_password_data['old_password']
        form = ChangePasswordForm(user=self.user, data=self.change_password_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['old_password'][0], "This field is required.")
        self.assertFalse(check_password(password=self.change_password_data['new_password1'], encoded=self.user.password))
        self.assertTrue(check_password(password=self.user_data['password1'], encoded=self.user.password))

    def test_change_password_with_empty_field_new_password1(self):
        del self.change_password_data['new_password1']
        form = ChangePasswordForm(user=self.user, data=self.change_password_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password1'][0], "This field is required.")
        self.assertFalse(check_password(password=self.change_password_data['new_password2'], encoded=self.user.password))
        self.assertTrue(check_password(password=self.user_data['password1'], encoded=self.user.password))

    def test_change_password_with_empty_field_new_password2(self):
        del self.change_password_data['new_password2']
        form = ChangePasswordForm(user=self.user, data=self.change_password_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password2'][0], "This field is required.")
        self.assertFalse(check_password(password=self.change_password_data['new_password1'], encoded=self.user.password))
        self.assertTrue(check_password(password=self.user_data['password1'], encoded=self.user.password))

    def test_change_password_with_mismatched_password(self):
        self.change_password_data['new_password1'] = 'mismatch_password'
        form = ChangePasswordForm(user=self.user, data=self.change_password_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['new_password2'][0], "The two password fields didn't match.")
        self.assertFalse(check_password(password=self.change_password_data['new_password1'], encoded=self.user.password))
        self.assertTrue(check_password(password=self.user_data['password1'], encoded=self.user.password))