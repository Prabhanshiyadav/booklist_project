from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Book
from .forms import BookForm
from django.core.paginator import Paginator
import csv
from reportlab.pdfgen import canvas


from reportlab.pdfgen import canvas

def book_list(request):
    query = request.GET.get('search')
    books = Book.objects.all().order_by('-id')  # or by 'title' or 'published_date'
    if query:
        books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    paginator = Paginator(books, 6)  # 6 books per page
    page = request.GET.get('page')
    books_page = paginator.get_page(page)

    return render(request, 'books/book_list.html', {'books': books_page})


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'books/book_form.html', {'form': form})

def export_books_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=books.csv'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Author', 'Published Date', 'Description'])

    for book in Book.objects.all():
        writer.writerow([book.title, book.author, book.published_date, book.description])

    return response

def export_books_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=books.pdf'

    p = canvas.Canvas(response)
    y = 800
    p.setFont("Helvetica", 12)

    for book in Book.objects.all():
        p.drawString(50, y, f"{book.title} | {book.author} | {book.published_date}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Add Book'})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'title': 'Edit Book'})




# ✅ Export to CSV
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=books.csv'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Author', 'Description', 'Published Date'])

    for book in Book.objects.all():
        writer.writerow([book.title, book.author, book.description, book.published_date])

    return response

# ✅ Export to PDF
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=books.pdf'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    y = 800
    p.drawString(100, y, "Books List:")
    y -= 30

    for book in Book.objects.all():
        line = f"{book.title} - {book.author} - {book.published_date}"
        p.drawString(100, y, line)
        y -= 20
        if y <= 40:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response




def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')
