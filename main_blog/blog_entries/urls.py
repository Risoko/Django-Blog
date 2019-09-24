from django.urls import path

from . import views

app_name = 'blog_entries'
urlpatterns = [
    path(route='entries/', view=views.AllArticleView.as_view(), name='all_entries'),
    path(route='create_article/', view=views.CreateArticleView.as_view(), name='creata_article'),
    path(route='entries/<int:pk>', view=views.MainBlogView.as_view(), name='article_details'),
    path(route='change_article/<int:pk>', view=views.ChangeBlogEntryView.as_view(), name="change_article")
]
