from django.core.management.base import BaseCommand

from apps.asx.models import Company


class Command(BaseCommand):
    help = 'Sync company data with ASX official.'

    def handle(self, *args, **options):
        Company.sync()
