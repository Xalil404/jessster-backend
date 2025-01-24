from django.contrib import admin
from .models import Post, Category, Comment
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('id','title', 'slug', 'comment_count', 'author', 'status', 'category', 'language', 'created_on')
    list_filter = ('status', 'category', 'language')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_on'
    ordering = ['status', '-created_on']
    summernote_fields = ('content',)
    list_editable = ('status',)  # Make the status field editable in the list view

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'language', 'slug')  # Added slug for visibility
    search_fields = ('name', 'slug')  # Allow searching by name and slug
    prepopulated_fields = {'slug': ('name',)}  # Auto-generate slug based on name



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'post', 'user_username', 'created_on', 'is_active')  # Access user details correctly
    list_filter = ('is_active', 'created_on')  # Use is_active as it is a BooleanField
    search_fields = ('content', 'user__username', 'user__email')  # Search by content and user info
    ordering = ['-created_on']  # Order by creation date, descending
    date_hierarchy = 'created_on'

    # Add a method to display the user's username in list_display
    def user_username(self, obj):
        return obj.user.username  # Access the 'username' attribute of the related User model
    user_username.admin_order_field = 'user__username'  # Allow sorting by username
    user_username.short_description = 'User'  # Display a readable name for this column
