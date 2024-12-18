from django.contrib import admin
from .models import Gallery, Category


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'head_image', 'created')
    ordering = ['-created']


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Category, CategoryAdmin)
