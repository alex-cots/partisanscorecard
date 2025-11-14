from django.core.management import BaseCommand, call_command
from core.models import CongressMembership

class Command(BaseCommand):
    help = """ Call other management commands to keep database up to date with new data."""

    def add_arguments(self, parser):
        parser.add_argument('congress-number', nargs='?', type=int, help='Congress number to process')

    def handle(self, *_args, **options):
        congress_number = options['congress-number']
        if congress_number is None:
            congress_number = (CongressMembership.objects
                                .order_by('-congress')
                                .values_list('congress', flat=True)[0])
            print(f"Defaulting to current congress {congress_number}.")
        call_command('fetch-congress', str(congress_number))
        call_command('load-lis-ids')
        call_command('load-votes', str(congress_number))
        call_command('calculate-stats', str(congress_number))
