from django.contrib import admin
from .models import Category, Article, Comment

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "created_at", "is_active", "category", "author")
    list_display_links = ("pk", "title")
    list_editable = ("is_active",)
    list_filter = ("category", )


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Article, ArticleAdmin)