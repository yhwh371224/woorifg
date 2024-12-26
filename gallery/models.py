import datetime
from django.db import models
from markdownx.utils import markdown
from PIL import Image  # 이미지 최적화를 위해 필요
import os


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
    title = models.CharField(max_length=30, blank=True, null=True)
    date = models.DateField(blank=True, null=True, default=datetime.date.today)
    head_image = models.ImageField(upload_to='gallery/%Y/%m/%d/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 먼저 이미지를 저장합니다.

        if self.head_image:  # 이미지가 존재할 때만 최적화 진행
            img_path = self.head_image.path
            img = Image.open(img_path)
            
            # 이미지 최적화 (WebP 변환)
            if img.format != 'WEBP':
                webp_path = os.path.splitext(img_path)[0] + '.webp'
                img.save(webp_path, 'WEBP', quality=80)
                self.head_image.name = os.path.relpath(webp_path, os.path.dirname(self.head_image.path))
                os.remove(img_path)  # 원본 JPG/PNG 삭제
            
            super().save(*args, **kwargs)  # 최적화된 이미지 경로를 저장합니다.

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

