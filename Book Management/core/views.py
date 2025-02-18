from django.shortcuts import render, redirect
from .models import Books
from .forms import BookForm
from django.db.models import Q

# Create your views here.

def book_list(request):
    books = Books.objects.all().order_by('id')
    return render(request, 'books/book_list.html', {'books': books})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('book_list')
    else:
        form = BookForm()
        return render(request, 'books/add_book.html', {'form': form})


def delete_book(request, book_id):
    book = Books.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')


def update_book(request, book_id):
    book = Books.objects.get(id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
        return render(request, 'books/update_book.html', {'form': form})


def search_book(request):
    books = Books.objects.all().order_by('id')
    if 'search' in request.GET:
        search = request.GET['search']
        # Using Q to combine queries for multiple fields
        books = Books.objects.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search) |
            Q(description__icontains=search) |
            Q(publication_year__icontains=search)
        )
    return render(request, 'books/book_list.html', {'books': books})



