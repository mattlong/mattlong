from django.contrib import admin
from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'is_published', 'published_date')
admin.site.register(Post, PostAdmin)
