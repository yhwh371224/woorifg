import datetime
from django.db import models
from markdownx.utils import markdown


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/gallery/category/{}/'.format(self.slug)

    class Meta:
        verbose_name_plural = 'categories'


class Gallery(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True, default=datetime.date.today)
    head_image = models.ImageField(upload_to='gallery/%Y/%m/%d/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return '{} :: {}'.format(self.title, self.category)

    def get_absolute_url(self):
        return '/gallery/{}/'.format(self.pk)

    def get_update_url(self):
        return self.get_absolute_url() + 'update/'

    def get_markdown_content(self):
        return markdown(self.content if hasattr(self, 'content') else '')

