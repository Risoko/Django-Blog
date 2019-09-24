from collections import namedtuple

from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.base import TemplateView, TemplateResponseMixin
from django.views.generic.detail import BaseDetailView, SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.http import Http404
from django.utils.translation import gettext_lazy as _

from blog_auth.views import MyFormView
from .forms import CreateArticleForm, CreateCommentForm, ChangeArtilceEntryForm, DeleteArticleForm, DeleteCommentForm, ChangeCommentForm
from .models import Article, Comment

operation_on_comments = namedtuple(
    typename='operation_on_comments',
    field_names='delete_comment edit_comment comment delete_form edit_form'
)


class AllArticleView(ListView):
    model = Article
    template_name = 'articles/show_article.html'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if not self.request.user.check_is_adult():
                return Article.objects.all().filter(for_adult=False)
            return Article.objects.all()
        return Article.objects.all().filter(for_adult=False)


class MainBlogView(SingleObjectMixin, TemplateView):
    model = Article
    model_comment = Comment
    create_comment_form_class = CreateCommentForm
    delete_article_form_class = DeleteArticleForm
    delete_comment_form_class = DeleteCommentForm
    change_comment_form_class = ChangeCommentForm
    template_name = 'articles/details_article.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated and self.object.for_adult:
            raise Http404(_('Not found page. You must log in or there is no such entry'))
        if request.POST.get('delete_article_pk'):
            return self.delete_article(request, *args, **kwargs)
        elif request.POST.get('delete_comment_pk'):
            return self.delete_comment(request, *args, **kwargs)
        elif request.POST.get('change_comment_pk'):
            return self.change_comment(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
        
    def get_create_comment_form(self):
        return self.create_comment_form_class(
            user=self.request.user,
            article=self.object,
            **self.get_form_kwargs()
        )

    def get_delete_article_form(self):
        return self.delete_article_form_class(
            article=self.object,
            **self.get_form_kwargs()
        )
        
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_user_comments(self, all_comments, user, owner_article=False):
        comments = []
        for comment in all_comments:
            if comment.check_the_owner(user):
                comments.append(operation_on_comments(
                        delete_comment=True,
                        edit_comment=True,
                        comment=comment,
                        edit_form=self.change_comment_form_class(comment=comment),
                        delete_form=self.delete_comment_form_class(comment=comment)
                    )
                )
            else:
                delete = False
                delete_form = None
                if owner_article:
                    delete = True
                    delete_form = self.delete_comment_form_class(comment=comment)
                comments.append(operation_on_comments(
                        delete_comment=delete,
                        edit_comment=False,
                        comment=comment,
                        delete_form=delete_form,
                        edit_form=None
                    )        
                )
        return comments

    def get_context_data(self, **kwargs):
        all_comments = self.get_all_comments_for_entry(self.object.id)
        print('comments', all_comments)
        if self.request.user.is_authenticated:
            kwargs.update({
                'add_comment': True,
                'create_comment_form': self.get_create_comment_form(),
                'comments': self.get_user_comments(all_comments=all_comments, user=self.request.user)
                }
            )
        else:
            kwargs.update({
                    'comments': all_comments
                }  
            )
        if self.object.check_the_owner(author=self.request.user):
            kwargs.update({
                    'owner': True,
                    'delete_article_form': self.get_delete_article_form(),
                    'comments': self.get_user_comments(all_comments=all_comments, user=self.request.user, owner_article=True)
                }
            )
        return super().get_context_data(**kwargs)

    def get_all_comments_for_entry(self, article_pk):
        return self.model_comment.objects.all().filter(article=article_pk)

    def post(self, request, *args, **kwargs):
        form = self.get_create_comment_form()
        return self.form_valid(form=form) if form.is_valid() else self.form_invalid(form=form)

    def form_valid(self, form):
        form.save()
        return redirect(to=reverse('blog_entries:article_details', args=[self.object.pk]))

    def form_invalid(self, form):
        return self.render_to_response(context=self.get_context_data())

    def delete_article(self, request, *args, **kwargs):
        delete_form = self.get_delete_article_form()
        if delete_form.is_valid():
            return self.form_delete_article_valid(form=delete_form)

    def delete_comment(self, request, *args, **kwargs):
        delete_form = self.delete_comment_form_class(data=request.POST)
        if delete_form.is_valid():
            return self.form_valid(form=delete_form)

    def change_comment(self, request, *args, **kwargs):
        comment = self.model_comment.objects.get(pk=request.POST['change_comment_pk'])
        change_comment_form = self.change_comment_form_class(data=request.POST, instance=comment )
        if change_comment_form.is_valid():
            return self.form_valid(form=change_comment_form)

    def form_delete_article_valid(self, form):
        form.save()
        return redirect(to=reverse('blog_entries:all_entries'))


@method_decorator(
    decorator=login_required(login_url=reverse_lazy('blog_auth:login')),
    name='dispatch'
    )
class ChangeBlogEntryView(BaseDetailView, TemplateResponseMixin, FormMixin):
    model = Article
    form_class = ChangeArtilceEntryForm
    template_name = 'articles/change_article.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.check_the_owner(author=request.user):
            raise KeyError
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class( 
            article=self.get_object(), 
            instance=self.object,
            **self.get_form_kwargs()  
        )

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        return self.form_valid(form=form) if form.is_valid() else self.form_invalid(form=form)

    def form_valid(self, form):
        form.save()
        print('zapisujeeee')
        return redirect(to=reverse('blog_entries:article_details', args=[self.object.pk]))

    def form_invalid(self, form):
        print('print')
        return self.render_to_response(context=self.get_context_data())

    def get_context_data(self, **kwargs):
        return FormMixin.get_context_data(self, **kwargs)


@method_decorator(
    decorator=login_required(login_url=reverse_lazy('blog_auth:login')),
    name='dispatch'
    )
class CreateArticleView(MyFormView):
    form_class = CreateArticleForm
    template_name = 'articles/create_article.html'

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(user=self.request.user, **self.get_form_kwargs()) # add user
