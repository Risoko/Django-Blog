from django.db import models

class ArticleManager(models.Manager):

    def create_article(self, author, title, entry, **extra_fields):
        article = self.model(
            author=author, 
            title=title, 
            entry=entry, 
            **extra_fields
        )
        article.save()
        return article

class CommentManager(models.Manager):

    def create_comment(self, owner, article, content_comment, **extra_fields):
        comment = self.model(
            owner=owner,
            article=article,
            content_comment=content_comment,
            **extra_fields
        )
        comment.save()
        return comment