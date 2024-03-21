# myapp/management/commands/preload_functions.py

from django.core.management.base import BaseCommand

import sys
sys.path.append('D:\\My Stuff\\UNI\\8th Semester\\FYP-II\\webapp\\webapp\\venv')
import dataset  # Import the entire python file
import votingsystem  # Import the entire python file

class Command(BaseCommand):
    help = 'Preload additional functions'

    def handle(self, *args, **kwargs):
        # Importing the files will execute their code
        self.stdout.write(self.style.SUCCESS('Additional functions preloaded successfully'))
