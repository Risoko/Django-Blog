from datetime import date

from django.test import TestCase

from blog_auth.forms import CreateProfileForm
from blog_auth.models import User

class TestCreateProfileForm(TestCase):

    def setUp(self):
        self.user = self._create_user()
        self.data_for_profile = {
            'first_name': 'Test',
            'last_name': 'Tester',
            'sex': 'M',
            'country': 'PL',
            'date_birth': date(
                year=1996,
                month=3,
                day=12
            )
        }
        
    def _create_user(self):
        return User.objects.create_user(
            username='tester',
            email='przemyslaww.rozyckii@gmail.com',
            password='tester123',
            nick='testowy',
        )

    def test_first_name_field_empty(self):
        del self.data_for_profile['first_name']
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['first_name'][0],
            "This field is required."
        )

    def test_first_name_field_if_is_too_short(self):
        self.data_for_profile['first_name'] = 'te'
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['first_name'][0],
            "Ensure this value has at least 3 characters (it has 2)."
        )

    def test_first_name_field_if_is_too_long(self):
        self.data_for_profile['first_name'] = 30 * 'te'
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['first_name'][0],
            "Ensure this value has at most 30 characters (it has 60)."
        )

    def test_first_name_field_with_digit(self):
        self.data_for_profile['first_name'] = 'tetek123'
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['first_name'][0],
            'First name must contain only letters.'
        )

    def test_first_name_field_with_bad_letter_case(self):
        self.data_for_profile['first_name'] = 'joHnY'
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        form.is_valid()
        print(form.errors)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.user.user_profile.first_name, 'Johny')
        self.assertTrue(self.user.is_active)

    def test_last_name_field_empty(self):
        del self.data_for_profile['last_name']
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['last_name'][0],
            "This field is required."
        )

    def test_last_name_field_if_is_too_short(self):
        self.data_for_profile['last_name'] = 'te'
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['last_name'][0],
            "Ensure this value has at least 3 characters (it has 2)."
        )

    def test_last_name_field_if_is_too_long(self):
        self.data_for_profile['last_name'] = 30 * 'te'
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['last_name'][0],
            "Ensure this value has at most 30 characters (it has 60)."
        )

    def test_last_name_field_with_digit(self):
        self.data_for_profile['last_name'] = 'tetek123'
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['last_name'][0],
            'Last name must contain only letters.'
        )

    def test_last_name_field_with_bad_letter_case(self):
        self.data_for_profile['last_name'] = 'KowAlSki'
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.user.user_profile.last_name, 'Kowalski')
        self.assertTrue(self.user.is_active)

    def test_form_with_correct_data(self):
        form = CreateProfileForm(user=self.user, data=self.data_for_profile)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.user.user_profile.first_name, self.data_for_profile['first_name'])
        self.assertEqual(self.user.user_profile.last_name, self.data_for_profile['last_name'])
        self.assertEqual(self.user.user_profile.date_birth, self.data_for_profile['date_birth'])
        self.assertEqual(self.user.user_profile.sex, self.data_for_profile['sex'])
        self.assertEqual(self.user.user_profile.country, self.data_for_profile['country'])
        self.assertTrue(self.user.is_active)
        





        






