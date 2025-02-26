from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.db.models import Q
from .permissions import book_delete_permission, book_update_permission, book_add_permission
import logging

logger = logging.getLogger(__name__)


# Create your views here.

def book_list(request):
    logger.info(f"Viewing Index Page, IP: {request.META.get('REMOTE_ADDR')}")

    title = request.GET.get('search_title')
    author = request.GET.get('search_author')

    filters = Q()

    if title and author:
        filters &= Q(title__icontains=title) & Q(author__icontains=author)
        logger.info(f'Search Title: "{title}", Search Author: {author}, IP: {request.META.get('REMOTE_ADDR')}')
    elif title:
        filters |= Q(title__icontains=title)
        logger.info(f'Search Title: "{title}", IP: {request.META.get('REMOTE_ADDR')}')
    elif author:
        filters |= Q(author__icontains=author)
        logger.info(f'Search Author: {author}, IP: {request.META.get('REMOTE_ADDR')}')

    if title or author:
        books = Book.objects.filter(filters).order_by('id')
        logger.info(f'Books found: {books.count()}')

    else:
        books = Book.objects.all().order_by('id')

    items_per_page = 10
    page = request.GET.get('page', 1)
    paginator = Paginator(books, items_per_page)

    try:
        books_page = paginator.page(page)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)

    return render(request, 'books/book_list.html',
                  {'books': books_page, 'title': title, 'author': author})


@login_required(login_url='login')
@book_add_permission
def add_book(request):
    logger.info(f"Started Adding Book, IP: {request.META.get('REMOTE_ADDR')}")
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            logger.info(f'Added Book: {book.title} by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
            return redirect('book_list')
    else:
        form = BookForm()

        return render(request, 'books/add_book.html', {'form': form})


@login_required(login_url='login')
@book_delete_permission
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    logger.info(f'Started Deleting Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')

    if request.method == 'POST':
        book.delete()
        logger.info(f'Deleted Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
        return redirect('book_list')


@login_required(login_url='login')
@book_update_permission
def update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    logger.info(f'Started Editing Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            logger.info(f'Edited Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
            return redirect('book_details', pk=book_id)
        else:
            logger.warning(f'Invalid form')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = BookForm(instance=book)
        return render(request, 'books/update_book.html', {'form': form, 'book': book})


def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    logger.info(f'Viewing Book "{book.title}" by {book.author}, IP: {request.META.get('REMOTE_ADDR')}')
    return render(request, 'books/book_details.html', {'book': book})
