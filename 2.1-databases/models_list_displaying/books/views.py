from django.shortcuts import render, redirect
from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    context = {
        'books': Book.objects.all()
    }
    return render(request, template, context)


def books_on_date_view(request, dt):
    template = 'books/books_list.html'

    books = Book.objects.all()
    all_pub_dates = sorted({book.pub_date.strftime('%Y-%m-%d') for book in books})

    index_date = all_pub_dates.index(dt.strftime('%Y-%m-%d'))

    pagi_dict = {'current': index_date}

    if 0 < index_date < len(all_pub_dates) - 1:
        pagi_dict['prev_p'] = all_pub_dates[index_date - 1]
        pagi_dict['next_p'] = all_pub_dates[index_date + 1]
    elif index_date == 0:
        pagi_dict['next_p'] = all_pub_dates[index_date + 1]
    elif index_date == len(all_pub_dates) - 1:
        pagi_dict['prev_p'] = all_pub_dates[index_date - 1]

    context = {
        'books': Book.objects.filter(pub_date=dt),
        'pagi_dict': pagi_dict
    }
    return render(request, template, context)


def index(request):
    return redirect('books')
