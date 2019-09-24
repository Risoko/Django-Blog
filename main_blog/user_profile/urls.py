from django.urls import path
from . import views

app_name = 'user_profile'
urlpatterns = [
    path(route='change_password/', view=views.ChangePasswordView.as_view(), name='change_password'),
    path(route='change_email/', view=views.ChangeEmailView.as_view(), name='change_email')
]