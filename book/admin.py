from django.contrib import admin
from django.contrib.admin import register
from django.utils.translation import gettext_lazy as _

from book.models import Book, Genre


@register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'stars', 'pages', 'published_at']
    search_fields = ['title', 'author']
    filter_horizontal = ['genres']
    fieldsets = [
        [_('basic'), {'fields': ['title', 'author']}],
        [_('Description'), {'fields': ['description']}],
        [_('Information'), {'fields': ['pages', 'stars', 'published_at']}],
        [_('Genres'), {'fields': ['genres']}],
        [_('Image'), {'fields': ['image_url']}],
    ]
    ordering = ['-published_at']


admin.site.register(Genre)
