from django.core.management.base import BaseCommand
import pandas as pd

# Load the dataset
file_path = 'pakistani_dataset_consolidated_augmented.xlsx'
dataset = pd.read_excel(file_path)

import sys
sys.path.append('D:\\My Stuff\\UNI\\8th Semester\\FYP-II\\webapp\\webapp\\venv')
import about_dataset  # Import the entire python file
import votingsystem  # Import the entire python file
import ensemble_classifier  # Import the entire python file
import multiple_inputs

class Command(BaseCommand):
    help = 'Preload additional functions'

    def handle(self, *args, **kwargs):
        # Preload the multiple_inputs function
        text_input = "Sample text"  # Provide a sample text for initialization
        title = "Sample title"  # Provide a sample title for initialization
        URL = "Sample URL"  # Provide a sample URL for initialization
        publisher_site = "Sample publisher site"  # Provide a sample publisher site for initialization
        claim_date = "Sample claim date"  # Provide a sample claim date for initialization
        multiple_inputs.multiple_inputs(text_input, title, URL, publisher_site, claim_date)
        # Indicate successful preloading
        self.stdout.write(self.style.SUCCESS('Additional functions preloaded successfully'))

