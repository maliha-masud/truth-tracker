from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import pyrebase

import sys
sys.path.append('D:\\My Stuff\\UNI\\8th Semester\\FYP-II\\webapp\\webapp\\venv')
from votingsystem import votingsystem
from ensemble_classifier import ensemble_classifier
from about_dataset import cols_dataset, visualize_dataset
from sentiment_analysis import sentiment_analysis, classify_personal_statement
from ner import ner
from multiple_inputs import multiple_inputs
from input_validation import is_gibberish, length_validation
# from news_classifier import classify_as_news

config = {
    "apiKey": "AIzaSyDA1e0JbHwZ5-5zoSf91DZCa-Run0XeHY8",
    "authDomain": "fyp-db-28850.firebaseapp.com",
    "databaseURL": "https://fyp-db-28850-default-rtdb.firebaseio.com",
    "projectId": "fyp-db-28850",
    "storageBucket": "fyp-db-28850.appspot.com",
    "messagingSenderId": "32336283099",
    "appId": "1:32336283099:web:a976a9efdef74a3b4353fe",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# Create your views here.
def home(request):
    return render(request, "home.html")

def login_form(request):
    return render(request, "login_form.html")

def project_overview(request):
    return render(request,"project_overview.html")

def user_manual(request):
    return render(request,"user_manual.html")

def faq(request):
    return render(request,"faq.html")

def input(request):
    return render(request, "input.html")

def output(request):
    text = request.GET.get('text', '')
    result = request.GET.get('result', '')
    sentiment = request.GET.get('sentiment', '')
    sentiment_score = request.GET.get('sentiment_score', '')
    personal_classification = "Personal Statement" if request.GET.get('personal_classification', '') == 1 else "Objective Statement"
    entities = request.GET.get('entities', '')
    ranked_entities = request.GET.get('ranked_entities', '')
    ensemble_result = request.GET.get('ensemble_result', '')

    # Fetch the multiple_classification and trustworthiness from the session
    multiple_classification = request.session.get('multiple_classification', '')
    trustworthiness = request.session.get('trustworthiness', '')
    outdated_warning = request.GET.get('outdated_warning', '')

    return render(request, 'output.html', {'text': text, 'result': result, 'sentiment': sentiment,
        'sentiment_score': sentiment_score, 'personal_classification': personal_classification, 
        'entities': entities, 'ranked_entities': ranked_entities, 'ensemble_result': ensemble_result,
        'multiple_classification': multiple_classification, 'trustworthiness': trustworthiness,
        'outdated_warning': outdated_warning}) #'is_news': is_news, 'news_score': news_score

def signin(request):
    return render(request, "signin_pg.html")

import os

def about_dataset(request):
    dataset_stats = cols_dataset()
    visualize_dataset()  # Call the visualize_dataset function
    image_path = settings.STATIC_URL + 'lineplot.png' #'webapp/static/lineplot.png' #'lineplot.png'  # Path of the saved image file

    context = {'dataset_stats': dataset_stats, 'image_path': image_path}
    return render(request, 'about_dataset.html', context) #render the template with the context

def visualize_data(request):
    return visualize_dataset()
    
@csrf_exempt  
def validate_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        length_validation_result = length_validation(text)
        
        response_data = {
            'is_valid_length': length_validation_result
        }
        
        if length_validation_result:
            is_gibberish_result = is_gibberish(text)
            response_data['is_gibberish'] = is_gibberish_result
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

from django.core.serializers.json import DjangoJSONEncoder
@csrf_exempt
def process_text(request):
    if request.method == 'POST':
        text_input = request.POST.get('text_input', '')
        title = request.POST.get('title', '')
        url = request.POST.get('url', '')
        publisher_site = request.POST.get('publisher_site', '')
        claim_date = request.POST.get('claim_date', '')
        sentiment, sentiment_score = sentiment_analysis(text_input)
        personal_classification = classify_personal_statement(text_input)
        result = votingsystem(text_input)
        entities, ranked_entities = ner(text_input)
        entities_json = json.dumps(entities, cls=DjangoJSONEncoder)
        ranked_entities_json = json.dumps(ranked_entities, cls=DjangoJSONEncoder)
        ensemble_result = ensemble_classifier(text_input)
        # is_news, news_score = classify_as_news(text_input)

        # Check if any additional field is entered by the user
        if title or url or publisher_site or claim_date:
            multiple_classification, trustworthiness, outdated_warning = multiple_inputs(text_input, title, url, publisher_site, claim_date)
        else:
            multiple_classification, trustworthiness, outdated_warning = '', '', ''

        data = {
            'text': text_input, 'result': result, 'sentiment': sentiment, 'sentiment_score': sentiment_score,
            'personal_classification': personal_classification, 'entities': entities_json,
            'ranked_entities': ranked_entities_json, 'ensemble_result': ensemble_result,
            'multiple_classification': multiple_classification, 'trustworthiness': trustworthiness,
            'outdated_warning': outdated_warning,
        } #'is_news': is_news, 'news_score': news_score
        request.session['multiple_classification'] = multiple_classification
        request.session['trustworthiness'] = trustworthiness
        return JsonResponse(data)
    return JsonResponse({'result': 'Invalid request method.'})
