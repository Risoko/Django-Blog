from django import forms

from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['pub_date', 'author', 'like', 'dislike']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        if not self.user.check_is_adult():
            self.fields['for_adult'].widget = forms.HiddenInput()

    def save(self, commit=True):
        article = super().save(commit=False)
        article.author = self.user
        if commit:
            article.save()
            return
        return article

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content_comment']

    def __init__(self, user, article, *args, **kwargs):
        self.user = user
        self.article = article
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.article = self.article
        comment.owner = self.user
        if commit:
            comment.save()
            return
        return comment

class ChangeArtilceEntryForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'entry']

    def __init__(self, article, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].initial = article.title
        self.fields['entry'].initial = article.entry

class DeleteArticleForm(forms.Form):
    delete_article_pk = forms.IntegerField(
        widget=forms.HiddenInput
    )

    def __init__(self, article=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if article is not None:
            self.fields['delete_article_pk'].initial = article.pk
        
    def save(self):
        article = Article.objects.get(pk=self.cleaned_data['delete_article_pk'])
        article.delete()
        return 

class ChangeCommentForm(forms.ModelForm):
    change_comment_pk = forms.IntegerField(
        widget=forms.HiddenInput,
    )
    class Meta:
        model = Comment
        fields = ['content_comment']

    def __init__(self, comment=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if comment is not None:
            self.fields['content_comment'].initial = comment.content_comment
            self.fields['change_comment_pk'].initial = comment.pk

class DeleteCommentForm(forms.Form):
    delete_comment_pk = forms.IntegerField(
        widget=forms.HiddenInput
    )

    def __init__(self, comment=None, *args, **kwargs):
        self.comment = comment
        super().__init__(*args, **kwargs)
        if comment is not None:
            self.fields['delete_comment_pk'].initial = comment.pk

    def save(self):
        comment = Comment.objects.get(pk=self.cleaned_data['delete_comment_pk'])
        comment.delete()
        return 

    
