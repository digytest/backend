from django.contrib import admin
from .models import Article, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Article)