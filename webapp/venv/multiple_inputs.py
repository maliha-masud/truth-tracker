import pandas as pd
from myapp.management.commands.preload import dataset
from urllib.parse import urlparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import class_weight
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import re

def multiple_inputs(text_input, title=None, URL=None, publisher_site=None, claim_date=None):
        # Convert result, trustworthiness, and outdated_warning to string for JSON serialization
        result = "Misleading"
        trustworthiness = "Source seems trustworthy"
        outdated_warning = "N/A"

        return result, trustworthiness, outdated_warning