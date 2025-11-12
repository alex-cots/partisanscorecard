from django.core.management import BaseCommand, call_command
from core.models import CongressMembership

class Command(BaseCommand):
    help = """ Call other management commands to keep database up to date with new data."""

    def handle(self, *_args, **_options):
        current_congress = (CongressMembership.objects
                            .order_by('-congress')
                            .values_list('congress', flat=True)[0])
        call_command('fetch-congress', str(current_congress))
        call_command('load-lis-ids')
        call_command('load-votes', str(current_congress))
        call_command('calculate-stats', str(current_congress))
