from django.contrib import admin

from .models import Post


# Register your models here.

# Documentation: https://docs.djangoproject.com/en/1.9/ref/contrib/admin/

class PostModelAdmin(admin.ModelAdmin):
    list_display = ("title", "timestamp", "updated")
    list_display_links = ["timestamp"]
    list_editable = ["title"]
    list_filter = ['title', 'updated']
    search_fields = ['title', 'content']

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
