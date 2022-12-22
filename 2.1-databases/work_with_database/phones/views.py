from django.shortcuts import render, redirect
from phones.models import Phone

def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort = request.GET.get('sort')
    template = 'catalog.html'
    if sort is None:
        context = {
            'phones': Phone.objects.all()
        }
    elif sort == 'min_price':
        context = {
            'phones': Phone.objects.order_by('price')
        }
    elif sort == 'max_price':
        context = {
            'phones': Phone.objects.order_by('-price')
        }
    elif sort == 'name':
        context = {
            'phones': Phone.objects.order_by('name')
        }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {
        'phone': Phone.objects.get(slug=slug)
    }
    return render(request, template, context)
