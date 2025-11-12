import os
from pathlib import Path
import json

from django.core.management.base import BaseCommand
from django.db import transaction
from core.enums import Chamber
from core.models import Bill, RollCall, Member, Vote
from core.management.utils.command_mixins import CongressArgMixin

VOTE_DATA_DIR = os.environ["VOTE_DATA_DIR"]

class Command(CongressArgMixin, BaseCommand):
    help = """
        Loads roll call and vote data into the database. Mostly will not overwrite existing data for
        performance reasons. Run the scraper first and set VOTE_DATA_DIR appropriately.
    """

    @transaction.atomic
    def handle(self, *_args, **options):
        congress_number = options["congress-number"]
        try:
            _loadvotes(congress_number)
        finally:
            print()


def _loadvotes(congress_number):
    path_list = Path(VOTE_DATA_DIR + f"/{congress_number}/votes").glob("**/data.json")
    total_bills = 0
    total_roll_calls = 0
    total_votes = 0
    for path in path_list:
        current_votes = 0
        short_dir = "/".join(path.parts[-3:])
        print(
            f"{total_bills} bills, {total_roll_calls} roll calls, {total_votes} votes. Processing {short_dir}",
            end="\r",
        )
        with path.open() as file:
            roll_call_json: dict = json.load(file)
            if roll_call_json["category"] == "quorum":
                # Quorum votes aren't partisan. Also 2023/h1 is causing an error due to an edge
                # case around former rep. McEachin.
                continue

            bill, bill_is_new = _save_bill(roll_call_json)
            if bill_is_new:
                total_bills += 1

            roll_call, roll_call_is_new = _save_roll_call(roll_call_json, bill)
            # Votes should already be loaded if the roll call record is not new.
            if not roll_call_is_new:
                continue
            total_roll_calls += 1
            for position in roll_call_json["votes"].keys():
                for vote_json in roll_call_json["votes"][position]:
                    if vote_json == "VP":
                        # Don't support VP votes.
                        continue
                    current_votes += 1
                    print(
                        f"{total_bills} bills, {total_roll_calls} roll calls, {total_votes} votes. Processing {short_dir} vote {current_votes}           ",
                        end="\r",
                    )
                    _vote, created = _save_vote(roll_call, position, vote_json)
                    if created:
                        total_votes += 1
    print(
        f"{total_bills} bills, {total_roll_calls} roll calls, {total_votes} votes.                                        "
    )


def _save_bill(roll_call_json: dict) -> tuple[Bill | None, bool]:
    """Store a bill record and return the record and a boolean indicating if the record is new.

    The title is sometimes missing so we upsert it when present. It's possible there is an edge
    case where the title changes in subsequent votes and we process the votes out of order, so we
    may need to revisit this if bill titles become more important for this project.
    """
    bill_json = roll_call_json.get("bill")
    if bill_json is None:
        return None, False

    defaults = {}
    title = bill_json.get("title")
    if not title:
        # Bill title is often found in the roll call subject for some reason.
        title = roll_call_json.get("subject")
    if title:
        defaults["title"] = title
    return Bill.objects.update_or_create(
        congress=bill_json["congress"],
        type=bill_json["type"],
        number=bill_json["number"],
        defaults=defaults,
    )


def _save_roll_call(roll_call_json: dict, bill: Bill | None) -> tuple[RollCall, bool]:
    """Store a roll call record and return the record and a boolean indicating if the record is new."""

    defaults = {
        "category": roll_call_json["category"],
        "chamber": Chamber.from_letter(roll_call_json["chamber"]),
        "congress": roll_call_json["congress"],
        "number": roll_call_json["number"],
        "question": roll_call_json["question"],
        "result": roll_call_json["result"],
        "timestamp": roll_call_json["date"],
    }
    if bill is not None:
        defaults["bill"] = bill
    return RollCall.objects.get_or_create(id=roll_call_json["vote_id"], defaults=defaults)


def _save_vote(roll_call: RollCall, position: str, vote_json: dict) -> tuple[Vote, bool]:
    """Store a vote record and return the record and a boolean indicating if the record is new."""
    try:
        member = Member.objects.get(pk=vote_json["id"])
    except Member.DoesNotExist:
        # Senators are found by LIS id... hopefully this will change some day.
        try:
            member = Member.objects.get(lis_id=vote_json["id"])
        except:
            print()
            print(vote_json["id"])
            raise
    except:
        print()
        print(vote_json)
        raise
    return Vote.objects.get_or_create(
        roll_call=roll_call, member=member, defaults={"position": position}
    )
