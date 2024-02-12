from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from book.views import BookDetailAPIView


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('api/', include(('API.urls', 'API'), namespace='api')),
    path('books/', TemplateView.as_view(template_name='books.html'), name='books'),
    path('books/detail/<int:pk>', BookDetailAPIView.as_view(), name='detail')
    # path('genres/', TemplateView.as_view(template_name='genres.html'), name='genres'),
]
