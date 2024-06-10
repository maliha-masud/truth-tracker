# Truth Tracker

Truth Tracker is a web platform for multi-class categorization of Pakistani news, aiming to apply the concepts of machine learning and NLP to verify news and help users understand what elements contribute to the final rulings.
## Features

- Dataset containing texts from Pakistani news and classification labels including true, mostly true, half true, misleading, satire, and false
- Ensemble classification method employing models of support vector machine, random forest, multinomial NB, and logistic regression
- NLP methods for sentiment analysis and named entity recognition (NER)
- Intuitive web app to enter text (and other related data) for instant results. Additionally, learn more about news fabrication, propaganda, and the fight against misinformation in Pakistan.

<div align="center">
  <video src="https://github.com/maliha-masud/truth-tracker/assets/121713404/4d6a8ac5-03ee-4e5e-bf16-4f26a1d0232b" controls>
    Your browser does not support the video tag.
  </video>
</div>
  
## Technologies/Libraries

The dataset is created by scraping the web, the analysis of text is done using ensemble machine learning models and NLP techniques, the front end is created using Django, and the chrome extension is created using Flask.

**Web Scraping:** Requests, Beautiful Soup, Selenium, Regular Expressions (Regex), Pandas
<p align="center">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/454c9b06-df95-4e50-bda9-d0da0174b2d3" alt="logo-beautifulsoup" width="135">&nbsp;
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/e23a46e9-c1b2-4f57-be20-acfcdb86f95f" alt="logo-selenium" width="35">&nbsp;&nbsp;&nbsp;
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/63b838d5-e606-4a71-a1a2-346c25ce2461" alt="logo-Pandas" width="115">
</p>

**Model Training:** scikit-learn, TensorFlow, Matplotlib, NumPy, Pandas
<p align="center">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/f7092dc8-56ab-4218-b8f4-ff6c3c2aa791" alt="logo-Scikit_learn" width="90">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/a26a957c-a1db-4079-8801-a457cbca1003" alt="logo-TensorFlow" width="110">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/700584c6-da44-4625-b618-bc1036241fb9" alt="logo-matplotlib" width="110">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/c4502e44-d416-4f4f-ae5d-73cd82630e9a" alt="logo-NumPy" width="110">&nbsp;&nbsp;
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/63b838d5-e606-4a71-a1a2-346c25ce2461" alt="logo-Pandas" width="115">
</p>

**NLP:** spaCy, TextBlob, NLTK, transformers (BERT), PyTorch
<p align="center">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/47d34bd1-1bde-42c3-9537-5804426ef905" alt="logo-spacy" width="85">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/e3698959-fc3e-42b3-9a31-411d4a55f21f" alt="logo-textblob" width="95">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/374a08da-7a03-40fb-b5b9-164cce5175f4" alt="logo-nltk" width="55">&nbsp;&nbsp;
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/af5974ee-ae95-418a-a073-543cef3312ee" alt="logo-pytorch" width="100">
</p>

**Client:** Django, HTML/CSS (Bootstrap CSS), JavaScript, jQuery

**Server:** Django
<p align="center">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/45605c4d-cdc8-4b62-9aa4-a116989005f5" alt="logo-django" width="90">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/49552b17-db6c-4b5d-825c-ad99252e2cfd" alt="logo-html-5-css-javascript" width="100">&nbsp;&nbsp;&nbsp;
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/daf0213a-c76c-4ff2-a661-50bad1717c54" alt="logo-bootstrap" width="60">&nbsp;&nbsp;
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/199c0113-095f-4552-b707-ca2591dbb3bd" alt="logo-jquery" width="60">
</p>

**Database**: Firebase, Pyrebase4
<p align="center">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/2230dbb4-d002-4f17-bf0b-ab833b16b5c4" alt="logo-Firebase" width="180">
</p>

**Authentication**: Firebase-Admin
<p align="center">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/4052ec0e-0e4a-4f46-ba12-a0b9ec7f2954" alt="logo-FirebaseAuth" width="180">
</p>

**Chrome Extension:** Flask
<p align="center">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/3542b920-4f46-4803-a6d2-18c2beb95352" alt="logo-flask" width="110">
</p>

**Data Visualization**: Matplotlib, Seaborn
<p align="center">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/700584c6-da44-4625-b618-bc1036241fb9" alt="logo-matplotlib" width="110">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/2766bbf4-50ad-4756-9f47-9d0b1a3eaac8" alt="logo-seaborn" width="140">
</p>

**Image Character Extraction**: PyTesseract, Tesseract OCR
<p align="center">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/f5cccebf-8270-4e68-a32f-6732f39591d2" alt="tesseract" width="110">
</p>

<details open>
    <summary><b>&nbsp;Package details</b></summary>
    <br>
    <ul>
        <li><b>Requests:</b> Python HTTP for Humans.</li>
        <li><b>Beautiful Soup/bs4:</b> Screen-scraping library</li>
        <li><b>Selenium (webdriver):</b> Automate web browser interaction from Python. Enables programmatically controlling web browsers for testing purposes or web scraping.</li>
        <li><b>Regular Expressions (Regex):</b> Searchable database of regular expressions.</li>
        <li><b>Pandas:</b> Powerful data structures for data analysis, time series, and statistics.</li>
        <li><b>scikit-learn:</b> A set of python modules for machine learning and data mining.</li>
        <li><b>TensorFlow:</b> TensorFlow is an open source machine learning framework for everyone.</li>
        <li><b>Matplotlib:</b> Python plotting package.</li>
        <li><b>NumPy:</b> Fundamental package for array computing in Python.</li>
        <li><b>spaCy:</b> Industrial-strength Natural Language Processing (NLP) in Python.</li>
        <li><b>TextBlob:</b> Simple, Pythonic text processing. Sentiment analysis, part-of-speech tagging, noun phrase parsing, and more.</li>
        <li><b>NLTK:</b> Natural Language Toolkit</li>
        <li><b>transformers:</b> State-of-the-art Machine Learning for JAX, PyTorch and TensorFlow.</li>
        <li><b>PyTorch:</b> Machine learning library for applications such as computer vision and natural language processing.</li>
        <li><b>Django:</b> A high-level Python web framework that encourages rapid development and clean, pragmatic design.</li>
        <li><b>jQuery:</b> JavaScript library</li>
        <li><b>Pyrebase4:</b> A simple python wrapper for the Firebase API with current deps.</li>
        <li><b>Firebase-Admin:</b> Firebase Admin Python SDK </li>
        <li><b>Flask:</b> A simple framework for building complex web applications.</li>
        <li><b>Seaborn:</b> Statistical data visualization.</li>
        <li><b>PyTesseract:</b> Python-tesseract is a python wrapper for Google's Tesseract OCR.</li>
        <li><b>Tesseract OCR:</b> A Python wrapper for Tesseract. </li>
        <li><b>langdetect:</b> Language detection library ported from Google's language-detection. </li>
    </ul>
</details>


## Run Locally

Create a folder for the project, and navigate into it
```bash
  cd project_name
```

#### Web app

Install Django

```bash
  pip install django
```

Start the Django project

```bash
  django-admin startproject project_name
```

Navigate into the created Django project

```bash
  cd project_name
```

Run the command to start the app

```bash
  python manage.py startapp myapp
```

Clone this project separately, and copy the webapp folder's contents (truth-tracker/webapp contents) into the subfolder named as your Django project

```bash
  git clone https://github.com/maliha-masud/truth-tracker
```

Navigate to the subfolder named as your Django project

```bash
  cd webapp
```

Make the required changes in the following files:
- `webapp/myapp/management/commands/preload.py`
- `webapp/venv/pyenv.confg`
- `webapp/myapp/views.py`

Install dependencies listed in `requirements.txt` into your local Python interpreter

```bash
  pip install -r requirements.txt
```
- May need to do manually (using `pip install` e.g. `pip install django`)

Activate venv

```bash
  venv/Scripts/activate
```

Run the batch file that runs the app

```bash
  .\run_server.bat
```

##

### Chrome Extension

Navigate to the chrome extension directory

```bash
  cd truth-tracker
  cd chrome-extension
```

Run the Flask application

```bash
  python app.py
```

Open Google Chrome.

Go to `chrome://extensions/`

Enable Developer mode (usually a toggle switch).

Click on the "Load unpacked" button.

Select the chrome-extension folder within the project directory.

→ You can now use the "Truth Tracker" extension.

## Acknowledgements

 - [Original Dataset](https://github.com/Adeelzafar/Fake-news-detection-on-Pakistani-news-using-machine-learning-and-deep-learning)
 - [Included Dataset](https://github.com/alisadia/Dashboard-Fake-News-Detector-/tree/main/infographic)
 - [The Dependent](https://dependent.pakistantoday.com.pk)
 - [Fact Check Explorer](https://toolbox.google.com/factcheck/explorer)
 - [Geo Fact Check](https://www.geo.tv/category/geo-fact-check)
 - [Politifact](https://www.politifact.com/)
 - [Uiverse.io](https://uiverse.io/)

## Related

Here are some related projects:

- [Fake news detection on Pakistani news using machine learning and deep learning](https://github.com/Adeelzafar/Fake-news-detection-on-Pakistani-news-using-machine-learning-and-deep-learning)
- [Pakistani Media Fake News Classification using Machine Learning Classifiers](https://ieeexplore.ieee.org/document/8966734)
- [Fake news detection in Urdu language using machine learning](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10280395/)
- [Improving Fake News Detection of Influential Domain via Domain- and Instance-Level Transfer](https://aclanthology.org/2022.coling-1.250/)
- [Litrl Browser](https://github.com/litrl/litrl_code)
## Appendix
### Color Reference:

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Deep Plum | ![#280337](https://via.placeholder.com/10/280337?text=+) &nbsp;#280337 |
| Indigo Violet | ![#4b2b79](https://via.placeholder.com/10/4b2b79?text=+) &nbsp;#4b2b79 |
| Rich Lavender | ![#631d79](https://via.placeholder.com/10/631d79?text=+) &nbsp;#631d79 |
| Midnight Blue | ![#2b0e92](https://via.placeholder.com/10/2b0e92?text=+) &nbsp;#2b0e92 |
| Periwinkle Blue | ![#7e61ff](https://via.placeholder.com/10/7e61ff?text=+) &nbsp;#7e61ff |
| Cornflower Blue | ![#3d83ff](https://via.placeholder.com/10/3d83ff?text=+) &nbsp;#3d83ff |
| Sky Blue | ![#2eadff](https://via.placeholder.com/10/2eadff?text=+) &nbsp;#2eadff |

##
<div align="right">
  <img src="https://github.com/maliha-masud/truth-tracker/assets/121713404/3475ba5c-70f4-49d1-937f-ee2881875f6a" alt="logo" width="65" style="vertical-align: middle;">
  <br>
  Truth Tracker
</div>
