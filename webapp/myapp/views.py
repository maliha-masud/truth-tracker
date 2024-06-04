from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from PIL import Image
import pytesseract

import sys
sys.path.append('{path to your venv e.g. D:\webapp\venv}')
from votingsystem import votingsystem
from ensemble_classifier import ensemble_classifier
from about_dataset import cols_dataset, visualize_dataset
from sentiment_analysis import sentiment_analysis, classify_personal_statement
from ner import ner
from multiple_inputs import multiple_inputs
from input_validation import is_gibberish, length_validation, language_detection
from trans_ur_to_en import translate_and_map_urdu_to_english
# from news_classifier import classify_as_news

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
    
def img_input(request):
    return render(request, "img_input.html")

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

    context = {
        'url_stats': dataset_stats[0],
        'title_stats': dataset_stats[1],
        'text_stats': dataset_stats[2],
        'rating_stats': dataset_stats[3],
        'site_stats': dataset_stats[4],
        'name_stats': dataset_stats[5]
    }
    return render(request, 'about_dataset.html', context)
    
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
            lang_detected = language_detection(text)
            response_data['lang_detected'] = lang_detected
        
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

# Ensure pytesseract uses the correct path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'{path to your tesseract exe e.g. C:\Program Files\Tesseract-OCR\tesseract.exe}'
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        temp_dir = 'temp'
        image_path = os.path.join(temp_dir, image.name)

        # Create the temp directory if it doesn't exist
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Save the uploaded image to the temporary location
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Open the image file and extract text
        img = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(img)

        # Delete the temporary image file
        os.remove(image_path)

        return JsonResponse({'extracted_text': extracted_text})

    return render(request, 'upload.html')