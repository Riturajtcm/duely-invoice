from django.test import TestCase
from django.core.management import call_command

class GlobalSetup(self):
    # Create some ponies and snakes here
    def setUp(self):
        # Load fixtures
        call_command('loaddata', 'tests/ponies')
