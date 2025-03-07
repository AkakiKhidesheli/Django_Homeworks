from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Book, Category, Language, BookLibrary
from .forms import BookForm
from django.db.models import Q
from .permissions import book_delete_permission, book_update_permission, book_add_permission
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

logger = logging.getLogger(__name__)


# Create your views here.

class BookListView(ListView):
    model = Book
    paginate_by = 10
    template_name = 'books/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):

        title = self.request.GET.get('search_title')
        author = self.request.GET.get('search_author')
        genre_id = self.request.GET.get('genre')
        language_id = self.request.GET.get('language')

        filters = Q()
        if title and author:
            filters &= Q(title__icontains=title) & Q(author__icontains=author)
        elif title:
            filters |= Q(title__icontains=title)
        elif author:
            filters |= Q(author__icontains=author)

        if genre_id:
            filters &= Q(genre_id=genre_id)

        if language_id:
            filters &= Q(language_id=language_id)

        if title or author or genre_id or language_id:
            books = self.model.objects.filter(filters).order_by('id')
            logger.info(f'Books found: {books.count()}')
        else:
            books = self.model.objects.all().order_by('id')

        return books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.GET.get('search_title', '')
        context['author'] = self.request.GET.get('search_author', '')
        context['genre_id'] = self.request.GET.get('genre', '')
        context['genres'] = Category.objects.all()
        context['language_id'] = self.request.GET.get('language', '')
        context['languages'] = Language.objects.all()
        return context


class CreateBookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/add_book.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        book = form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_details.html'

class DeleteBookView(DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')

class UpdateBookView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/update_book.html'

    def get_success_url(self):
        success_url = reverse_lazy('book_details', kwargs={'pk': self.object.pk})
        return success_url


# def book_list(request):
#     logger.info(f"Viewing Index Page, IP: {request.META.get('REMOTE_ADDR')}")
#
#     title = request.GET.get('search_title')
#     author = request.GET.get('search_author')
#     genre_id = request.GET.get('genre')
#     genres = Category.objects.all()
#     language_id = request.GET.get('language')
#     languages = Language.objects.all()
#
#     filters = Q()
#
#     if title and author:
#         filters &= Q(title__icontains=title) & Q(author__icontains=author)
#         logger.info(f'Search Title: "{title}", Search Author: {author}, IP: {request.META.get('REMOTE_ADDR')}')
#     elif title:
#         filters |= Q(title__icontains=title)
#         logger.info(f'Search Title: "{title}", IP: {request.META.get('REMOTE_ADDR')}')
#     elif author:
#         filters |= Q(author__icontains=author)
#         logger.info(f'Search Author: {author}, IP: {request.META.get('REMOTE_ADDR')}')
#
#     if genre_id:
#         genre = Category.objects.filter(id=genre_id)
#         genre = genre.first()
#         logger.info(f'Search Genre: {genre}, IP: {request.META.get('REMOTE_ADDR')}')
#         filters &= Q(genre_id=genre_id)
#
#     if language_id:
#         language = Language.objects.filter(id=language_id)
#         language = language.first()
#         logger.info(f'Search Language: {language}, IP: {request.META.get('REMOTE_ADDR')}')
#         filters &= Q(language_id=language_id)
#
#     if title or author or genre_id or language_id:
#         books = Book.objects.filter(filters).order_by('id')
#         logger.info(f'Books found: {books.count()}')
#     else:
#         books = Book.objects.all().order_by('id')
#
#     items_per_page = 10
#     page = request.GET.get('page', 1)
#     paginator = Paginator(books, items_per_page)
#
#     try:
#         books_page = paginator.page(page)
#     except PageNotAnInteger:
#         books_page = paginator.page(1)
#     except EmptyPage:
#         books_page = paginator.page(paginator.num_pages)
#
#     return render(request, 'books/book_list.html', {
#         'books': books_page,
#         'title': title,
#         'author': author,
#         'genre_id': genre_id,
#         'genres': genres,
#         'language_id': language_id,
#         'languages': languages,
#     })


# @login_required(login_url='login')
# @book_add_permission
# def add_book(request):
#     logger.info(f"Started Adding Book, IP: {request.META.get('REMOTE_ADDR')}")
#     if request.method == 'POST':
#         form = BookForm(request.POST, request.FILES)
#         if form.is_valid():
#             book = form.save()
#             logger.info(f'Added Book: {book.title} by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
#             return redirect('book_list')
#     else:
#         form = BookForm()
#
#         return render(request, 'books/add_book.html', {'form': form})


# @login_required(login_url='login')
# @book_delete_permission
# def delete_book(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#
#     logger.info(f'Started Deleting Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
#
#     if request.method == 'POST':
#         book.delete()
#         logger.info(f'Deleted Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
#         return redirect('book_list')


# @login_required(login_url='login')
# @book_update_permission
# def update_book(request, book_id):
#     book = Book.objects.get(id=book_id)
#     logger.info(f'Started Editing Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
#     if request.method == 'POST':
#         form = BookForm(request.POST, request.FILES, instance=book)
#         if form.is_valid():
#             book = form.save()
#             logger.info(f'Edited Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
#             return redirect('book_details', pk=book_id)
#         else:
#             logger.warning(f'Invalid form')
#             return redirect(request.META.get('HTTP_REFERER'))
#     else:
#         form = BookForm(instance=book)
#         return render(request, 'books/update_book.html', {'form': form, 'book': book})


# def book_details(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     logger.info(f'Viewing Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
#     return render(request, 'books/book_details.html', {'book': book})


@login_required(login_url='login')
def buy_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if book.not_in_stock():
        messages.error(request, 'Book not available')
        return redirect('/')

    book_library, created = BookLibrary.objects.get_or_create(book=book, user=request.user)

    if created:
        book_library.book_count = 1
    else:
        book_library.book_count += 1

    book_library.save()

    book.book_count -= 1
    book.save()

    send_mail('Order Confirmation',
              f'{request.user.username} has successfully bought book "{book.title}" by {book.author}',
              settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=False)

    return redirect('book_list')
