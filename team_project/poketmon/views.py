from django.shortcuts import render, redirect
from datetime import datetime
# Create your views here.


def main(request):
    current_time = datetime.now()
    return render(request, 'poketmon/index.html', {'date': current_time})


def type(request):
    img_url = {'imgs': ['pie_types_dist.png']}
    return render(request, 'poketmon/index.html', img_url)


def bmi(request):
    img_url = {'imgs': ['BMI_dist.png', 'gender_BMI_dist.png']}
    return render(request, 'poketmon/index.html', img_url)


def size(request):
    img_url = {'imgs': ['scatter_size_dist.png']}
    return render(request, 'poketmon/index.html', img_url)

