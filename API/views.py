from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from API.serializers import BookListSerializer, GenreSerializer
from rest_framework.generics import ListAPIView
from book.models import Book, Genre
from scraper import scrape
import asyncio


def scrape_pages(request):
    query = request.GET.get('Key')
    data = asyncio.run(scrape(query))

    for item in data:
        try:
            book = Book(title=item['title'], author=item['author'], description=item['description'],
                        stars=item['stars'], pages=item['pages'], published_at=item['published_at'],
                        image_url=item['image_url'])
            book.save()

            for name, url in item['genres']:
                genre, _ = Genre.objects.get_or_create(name=name, url=url)
                book.genres.add(genre)

        except IntegrityError:
            continue

    response_data = {
        'message': 'Scraping completed.',
    }
    return JsonResponse(response_data, status=200)


class BookListAPIView(ListAPIView):
    queryset = Book.objects.all().order_by('-published_at')
    serializer_class = BookListSerializer

    def get_queryset(self):
        query = self.request.query_params.get('Key', '').strip()
        filter_query = Q()
        for word in query.split():
            filter_query |= (Q(title__icontains=word) | Q(author__icontains=word) | Q(genres__name__icontains=word))
        return self.queryset.filter(filter_query).distinct()


class GetPostCategoryAPIView(ListAPIView):
    queryset = Genre.objects.all().order_by('-name')
    serializer_class = GenreSerializer

    def get_queryset(self):
        genre = self.request.query_params.get('Key', None)
        return self.queryset.filter(category__name__icontains=genre)
