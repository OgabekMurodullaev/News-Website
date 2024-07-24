from django.contrib import admin
from .models import Category, News, Contact

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_time', 'slug', 'status', 'category']
    list_filter = ['status', 'publish_time', 'created_time']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'body']
    ordering = ['status', 'publish_time']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Contact)
