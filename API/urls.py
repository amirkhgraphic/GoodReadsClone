from django.urls import path
from API.views import scrape_pages, BookListAPIView

urlpatterns = [
    path('scrape/', scrape_pages, name='scrape'),
    path('list/', BookListAPIView.as_view(), name='list'),
]
