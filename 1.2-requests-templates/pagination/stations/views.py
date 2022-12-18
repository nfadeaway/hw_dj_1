from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

import csv


bus_station_list = []
with open(settings.BUS_STATION_CSV, newline='', encoding='utf-8') as data_file:
    file_rows = csv.DictReader(data_file)
    for row in file_rows:
        bus_station_list.append(row)
def index(request):
    return redirect(reverse('bus_stations'))

def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(bus_station_list, 10)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page.object_list,
        'page': page
    }
    return render(request, 'stations/index.html', context)
