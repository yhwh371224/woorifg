import datetime
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/review/category/{}/'.format(self.slug)

    class Meta:
        verbose_name_plural = 'categories'


class Post(models.Model):
    content = MarkdownxField()
    name = models.CharField(max_length=100, blank=False, null=True)
    title = models.CharField(max_length=100, blank=False, null=True)
    date = models.DateField(blank=True, null=True, default=datetime.date.today)
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return '/review/{}/'.format(self.pk)

    def get_update_url(self):
        return self.get_absolute_url() + 'update/'

    def get_markdown_content(self):
        return markdown(self.content)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = MarkdownxField()
    author = models.CharField(max_length=100, blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_markdown_content(self):
        return markdown(self.text)

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-id-{}'.format(self.pk)
    
