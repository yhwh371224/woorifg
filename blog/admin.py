from django.contrib import admin
from .models import Members, Bulletin, Pdf


class MembersAdmin(admin.ModelAdmin):
    list_display = ['english_name', 'korean_name', 'contact', 'email', 'suburb']
    search_fields = ['english_name', 'korean_name', 'contact', 'email', 'suburb']
    ordering = ['-created']


class BulletinAdmin(admin.ModelAdmin):
    list_display = ('date', 'pdf_file', 'created')
    ordering = ['-created']


class PdfAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'pdf_file', 'created')
    ordering = ['-created']


admin.site.register(Members, MembersAdmin)
admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Pdf, PdfAdmin)