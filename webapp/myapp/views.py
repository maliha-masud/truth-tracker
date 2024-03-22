from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

import sys
sys.path.append('D:\\My Stuff\\UNI\\8th Semester\\FYP-II\\webapp\\webapp\\venv')
from votingsystem import votingsystem
from sentiment_analysis import sentiment_analysis, classify_personal_statement

# Create your views here.
def home(request):
    return render(request, "home.html")

def login_form(request):
    return render(request, "login_form.html")

def input(request):
    return render(request, "input.html")

def output(request):
    # Get the entered text, result, sentiment, and sentiment score from the query parameters
    text = request.GET.get('text', '')
    result = request.GET.get('result', '')
    sentiment = request.GET.get('sentiment', '')
    sentiment_score = request.GET.get('sentiment_score', '')
    personal_classification = "Personal Statement" if request.GET.get('personal_classification', '') == 1 else "Objective Statement"
    return render(request, 'output.html', {'text': text, 'result': result, 'sentiment': sentiment, 'sentiment_score': sentiment_score, 'personal_classification': personal_classification})

def signin(request):
    return render(request, "signin_pg.html")

def project_overview(request):
    return render(request,"project_overview.html")

def user_manual(request):
    return render(request,"user_manual.html")

def faq(request):
    return render(request,"faq.html")
    
@csrf_exempt
def process_text(request):
    if request.method == 'POST':
        text_input = request.POST.get('text_input', '')
        sentiment, sentiment_score = sentiment_analysis(text_input)
        personal_classification = classify_personal_statement(text_input)
        result = votingsystem(text_input)
        data = {
            'text': text_input,
            'result': result,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'personal_classification': personal_classification
        }
        return JsonResponse(data)
        # return JsonResponse({'result': result})
    return JsonResponse({'result': 'Invalid request method.'})
