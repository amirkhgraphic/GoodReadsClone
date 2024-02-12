from django.views.generic import DetailView
from book.models import Book


class BookDetailAPIView(DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.filter(id=self.kwargs['pk'])
