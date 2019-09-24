from django.urls import path

from . import views

app_name = 'blog_auth'
urlpatterns = [
    path(route='registration/', view=views.SignUpView.as_view(), name='registartion'),
    path(route='login/create_profile/', view=views.CreateProfileView.as_view(), name='create_profile'),
    path(route='login/', view=views.SignInView.as_view(), name='login'),
    path(route='reset_password/', view=views.ResetPasswordView.as_view(), name='reset_password'),
    path(route='', view=views.test , name='main')
]
