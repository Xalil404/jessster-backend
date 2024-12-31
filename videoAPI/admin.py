from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'video', 'language')
    search_fields = ('title',)
    list_filter = ('created_at',)

admin.site.register(Video, VideoAdmin)
