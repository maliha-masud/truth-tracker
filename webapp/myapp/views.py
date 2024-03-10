from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import sys
sys.path.append('D:\\My Stuff\\UNI\\8th Semester\\FYP-II\\webapp\\webapp\\venv')
from votingsystem import votingsystem

# Create your views here.
def home(request):
    return render(request, "home.html")

def login_form(request):
    return render(request, "login_form.html")

def input(request):
    return render(request, "input.html")

def signin(request):
    return render(request, "signin_pg.html")

def about_dataset(request):
    return render(request, "about_dataset.html")

@csrf_exempt
def process_text(request):
    if request.method == 'POST':
        text_input = request.POST.get('text_input', '')
        # print(f"Received text: {text_input}")  # Log the received text to the console
        result = votingsystem(text_input)
        return JsonResponse({'result': result})
    return JsonResponse({'result': 'Invalid request method.'})