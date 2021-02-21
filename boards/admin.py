from django.contrib import admin
from .models import *

class ImageInLineAdmin(admin.TabularInline):
    model = PostImage
    fields = ('image',)
    max_num = 5

@admin.register(Post)
class PostAsmin(admin.ModelAdmin):
    inlines = [ImageInLineAdmin, ]
    list_filter = ('created_by', 'created_at')

admin.site.register(Boards)
admin.site.register(Topic)
