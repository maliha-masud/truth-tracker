
# Truth Tracker

Truth Tracker is a web platform for multi-class categorization of Pakistani news, aiming to apply the concepts of machine learning and NLP to verify news and help users understand what elements contribute to the final rulings.
## Features

- Dataset containing texts from Pakistani news and classification labels including true, mostly true, half true, misleading, satire, and false
- Ensemble classification method employing models of support vector machine, random forest, multinomial NB, and logistic regression
- NLP methods for sentiment analysis and named entity recognition (NER)
- Intuitive web app to enter text (and other related data) for instant results. Additionally, learn more about news fabrication, propaganda, and the fight against misinformation.
## Technologies/Libraries

The dataset is created by scraping the web, the analysis of text is done using ensemble machine learning models and NLP techniques, the front end is created using Django, and the chrome extension is created using Flask.

**Web Scraping:** Requests, Beautiful Soup, Selenium, Regular Expressions (Regex), Pandas

**Model Training:** scikit-learn, TensorFlow, Matplotlib, NumPy, Pandas

**NLP:** spaCy, TextBlob, NLTK, transformers (BERT), PyTorch

**Client:** Django, HTML/CSS (Bootstrap CSS), JavaScript, jQuery

**Server:** Django

**Database**: Firebase

**Chrome Extension:** Flask

**Data Visualization**: Matplotlib, Seaborn

<details open>
    <summary>Want to ruin the surprise?</summary>
    <br>
    Well, you asked for it!
</details>


## Run Locally

Web app

Clone the project

```bash
  git clone https://github.com/maliha-masud/truth-tracker
```

Go to the project directory

```bash
  cd truth-tracker
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Navigate to the web app

```bash
  cd webapp
```

Activate venv

```bash
  venv/Scripts/activate
```

Run the batch file that runs the app

```bash
  .\run_server.bat
```

Make the required changes in the following files:
- `webapp/myapp/management/commands/preload.py`
- `webapp/venv/pyenv.confg`
- `webapp/myapp/views.py`

Chrome Extension

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

Go to `chrome://extensions/`.

Enable Developer mode (usually a toggle switch).

Click on the "Load unpacked" button.

Select the chrome-extension folder within the project directory.

You can now use the "Truth Tracker" extension.

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
Color Reference:

| Color             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Deep Plum | ![#280337](https://via.placeholder.com/10/280337?text=+) #280337 |
| Indigo Violet | ![#4b2b79](https://via.placeholder.com/10/4b2b79?text=+) #4b2b79 |
| Rich Lavender | ![#631d79](https://via.placeholder.com/10/631d79?text=+) #631d79 |
| Midnight Blue | ![#2b0e92](https://via.placeholder.com/10/2b0e92?text=+) #2b0e92 |
| Periwinkle Blue | ![#7e61ff](https://via.placeholder.com/10/7e61ff?text=+) #7e61ff |
| Cornflower Blue | ![#3d83ff](https://via.placeholder.com/10/3d83ff?text=+) #3d83ff |
| Sky Blue | ![#2eadff](https://via.placeholder.com/10/2eadff?text=+) #2eadff |

## 
![Logo](https://)