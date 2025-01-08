from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'video', 'language')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'status', 'language')
    list_editable = ('status',)  # Make the status field editable in the list view

admin.site.register(Video, VideoAdmin)
