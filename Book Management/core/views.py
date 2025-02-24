from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.db.models import Q
from .permissions import book_delete_permission, book_update_permission, book_add_permission
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def book_list(request):

    logger.info('Viewing Index Page')

    title = request.GET.get('search_title')
    author = request.GET.get('search_author')

    logger.info(f'Search Title: {title}, Search Author: {author}')

    filters = Q()

    if title and author:
        filters &= Q(title__icontains=title) & Q(author__icontains=author)
    elif title:
        filters |= Q(title__icontains=title)
    elif author:
        filters |= Q(author__icontains=author)

    if title or author:
        books = Book.objects.filter(filters).order_by('id')
    else:
        books = Book.objects.all().order_by('id')

        logger.info(f'Books found: {books.count()}')

    return render(request, 'books/book_list.html', {'books': books})

    # if searching_title and searching_author:
    #     books = Book.objects.filter(
    #         Q(title__icontains=searching_title) & Q(author__icontains=searching_author)).order_by('id')
    # elif searching_title:
    #     books = Book.objects.filter(Q(title__icontains=searching_title)).order_by('id')
    # elif searching_author:
    #     books = Book.objects.filter(Q(author__icontains=searching_author))
    # else:
    #     books = Book.objects.all().order_by('id')


@login_required(login_url='login')
@book_add_permission
def add_book(request):
    if request.method == 'POST':
        logger.info('Started Adding Book')
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            logger.info(f'Added Book: {book.title} by {book.author}')
            return redirect('book_list')
    else:
        form = BookForm()

        return render(request, 'books/add_book.html', {'form': form})


@login_required(login_url='login')
@book_delete_permission
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    logger.info(f'Started Deleting Book {book.title} by {book.author}')

    if request.method == 'POST':
        book.delete()
        logger.info(f'Deleted Book {book.title} by {book.author}')
        return redirect('book_list')


@login_required(login_url='login')
@book_update_permission
def update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    logger.info(f'Started Editing Book {book.title} by {book.author}')
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            logger.info(f'Edited Book {book.title} by {book.author}')
            return redirect('book_details', pk=book_id)
        else:
            logger.warning(f'Invalid form')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = BookForm(instance=book)
        return render(request, 'books/update_book.html', {'form': form, 'book': book})


# def search_book(request):
#     books = Books.objects.all().order_by('id')
#     if 'search_title' in request.GET:
#         search = request.GET['search_title']
#         books = Books.objects.filter(
#             Q(title__icontains=search) |
#             Q(author__icontains=search) |
#             Q(description__icontains=search) |
#             Q(publication_year__icontains=search) |
#             Q(genre__name__icontains=search)
#         )
#     return render(request, 'books/book_list.html', {'books': books})


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    logger.info(f'Viewing Book {book.title} by {book.author}')
    return render(request, 'books/book_details.html', {'book': book})
