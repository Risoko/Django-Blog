from datetime import date

from django.test import TestCase
from django.contrib.auth.hashers import check_password

from blog_auth.forms import PasswordResetForm
from blog_auth.models import User

class TestPasswordResetForm(TestCase):

    def setUp(self):
        self.user = self._create_user()
        self.data_for_reset = {
            'email': self.user.email,
            'username': self.user.username
        }

    def _create_user(self):
        return User.objects.create_user(
            username='tester',
            email='przemyslaww.rozyckii@gmail.com',
            password='tester123',
            nick='testowy'
        )

    def test_with_empty_email_field(self):
        del self.data_for_reset['email'] 
        form = PasswordResetForm(data=self.data_for_reset)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], "This field is required.")

    def test_with_username_email_field(self):
        del self.data_for_reset['username'] 
        form = PasswordResetForm(data=self.data_for_reset)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'][0], "This field is required.")

    def test_with_mismached_email_and_username(self):
        self.data_for_reset['email'] = 'przemek.pol@op.pl'
        form = PasswordResetForm(data=self.data_for_reset)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['__all__'][0],
            "The user with the given e-mail address or name does not exist."
        )

    def test_form_with_correct_data(self):
        form = PasswordResetForm(data=self.data_for_reset)
        form.is_valid()
        self.assertTrue(form.is_valid())
        new_password = form.save()
        user = User.objects.get(nick='testowy')
        self.assertFalse(check_password(password='tester123', encoded=user.password))
        self.assertTrue(check_password(password=new_password, encoded=user.password))


        


    

    

    

    
