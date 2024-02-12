from django.db import models
from datetime import date


class Genre(models.Model):
    name = models.CharField(max_length=127)
    url = models.URLField(null=True)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=127)
    description = models.TextField(null=True)
    genres = models.ManyToManyField(Genre, related_name='books')
    stars = models.CharField(max_length=7, null=True)
    pages = models.IntegerField(null=True)
    published_at = models.DateField(default=date.today, null=True)
    image_url = models.URLField(null=True)

    def __str__(self):
        return f'{self.title} - {self.author}'

    class Meta:
        unique_together = ('title', 'author')
