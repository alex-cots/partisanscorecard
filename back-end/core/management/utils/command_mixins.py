from django.core.management.base import BaseCommand


class CongressArgMixin(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("congress-number", help="congress number is required.", type=int)
        super().add_arguments(parser)
