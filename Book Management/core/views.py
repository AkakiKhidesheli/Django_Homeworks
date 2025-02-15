from django.shortcuts import render, redirect
from .models import Books
from .forms import BookForm


# Create your views here.

def book_list(request):
    books = Books.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
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