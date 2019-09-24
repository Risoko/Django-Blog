from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

from blog_auth.models import User
from .managers import ArticleManager, CommentManager
from .validators import check_is_digit_validator


class Article(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    pub_date = models.DateField(
        verbose_name=_('publish date'),
        help_text=_('Enter the publication date of the article.'),
        default=now
    )
    like = models.SmallIntegerField(
        verbose_name=_('you like it'),
        default=0
    )
    dislike = models.SmallIntegerField(
        verbose_name=_('you dislike it'),
        default=0
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=300,
        help_text=_('Enter title.'),
        validators=[MinLengthValidator(limit_value=10), check_is_digit_validator]
    )
    entry = models.TextField(
        verbose_name=_('blog entry'),
        help_text=_('Your blog entry'),
        validators=[MinLengthValidator(limit_value=200), check_is_digit_validator]
    )
    for_adult = models.BooleanField(
        verbose_name=_('adult content'),
        default=False
    )
    objects = ArticleManager()

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ['-pub_date']
    
    def check_the_owner(self, author):
        return self.author.username == author.username or author.is_superuser

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(
        to=Article,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    pub_date = models.DateField(
        verbose_name=_('publish date'),
        help_text=_('Enter the publication date of the article.'),
        default=now
    )
    content_comment = models.CharField(
        verbose_name=_('comment'),
        max_length=400,
        validators=[MinLengthValidator(limit_value=10), check_is_digit_validator],
        help_text=_('Comment for entry blog.')
    )
    objects = CommentManager()

    def check_the_owner(self, author):
        return self.owner.username == author.username or author.is_superuser

    def __str__(self):
        return self.content_comment

    def __lt__(self, other):
        return self.pub_date < other.pub_date





    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['-pub_date']






