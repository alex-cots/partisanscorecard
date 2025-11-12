from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from core.models import CongressMembership, Member, MemberStats, RollCall
from core.management.utils.command_mixins import CongressArgMixin


class Command(CongressArgMixin, BaseCommand):
    help = "Calculates and saves democratic and republican majority postions for every roll call vote."

    @transaction.atomic
    def handle(self, *_args, **options):
        congress_number = options["congress-number"]
        try:
            roll_call_count = _calculate_majority_positions(congress_number)
            print(f"Processed {roll_call_count} roll calls. Calculating member stats.")
            _calculate_member_stats(congress_number)
        finally:
            print()

def _calculate_majority_positions(congress_number):
    # Skip already calculated roll calls since the voting record shouldn't change over time.
    roll_calls_to_process = RollCall.objects.filter(
        Q(dem_maj_position="") | Q(repub_maj_position=""), congress=congress_number
    )
    print(f"{len(roll_calls_to_process)} roll calls to process.")
    roll_call_count = 0
    for rollCall in roll_calls_to_process:
        roll_call_count += 1
        print(f"Processing roll call number {roll_call_count}.", end="\r")
        rollCall.calculate_majority_positions(save=True)
    return roll_call_count

def _calculate_member_stats(congress_number):
    # Re-process all members in case we got new voting data.
    queryset = CongressMembership.objects.filter(congress=congress_number).prefetch_related("member")
    print(f"{len(queryset)} terms to process.")
    processed_member_count = 0
    for congress_membership in queryset:
        processed_member_count += 1
        print(
            f"Processing member number {processed_member_count}, {congress_membership.member}.                     ",
            end="\r",
        )
        MemberStats.create_from_congress_membership(congress_membership, upsert=True)

    print(f"Processed {processed_member_count} members. Calculating member loyalty ranks.                ")
    MemberStats.objects.calculate_loyalty_ranks(congress_number)
    print("Complete.", end='')
