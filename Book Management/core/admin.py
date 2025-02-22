from django.contrib import admin
from .models import Book


# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'shelf', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('genre',)


admin.site.register(Book, BookAdmin)
