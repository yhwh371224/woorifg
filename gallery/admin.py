from django.contrib import admin
from .models import Gallery, Category


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Gallery)
admin.site.register(Category, CategoryAdmin)
