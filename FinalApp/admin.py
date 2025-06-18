from django.contrib import admin
from .models import Blog
from datetime import datetime, date
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

@admin.register(Blog)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'picture', 'created_at', 'updated_at', 'author')
    search_fields = ('title__startwith',)
