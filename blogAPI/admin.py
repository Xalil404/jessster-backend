from django.contrib import admin
from .models import Post, Category
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('id','title', 'author', 'status', 'category', 'language', 'created_on')
    list_filter = ('status', 'category', 'language')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_on'
    ordering = ['status', '-created_on']
    summernote_fields = ('content',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'language', 'slug')  # Added slug for visibility
    search_fields = ('name', 'slug')  # Allow searching by name and slug
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug based on name
