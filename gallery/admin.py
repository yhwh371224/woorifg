from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Gallery


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    search_fields = ['title', 'date']
    ordering = ['-created']


class MyAdminSite(AdminSite):
    site_header = 'NewCovenant administration'


admin.site.register(Gallery, GalleryAdmin)
