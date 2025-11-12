import os
import requests
from core.enums import Chamber
from core.models import CongressMembership

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from core.models import Member
from core.management.utils.command_mixins import CongressArgMixin

CONGRESS_GOV_API_KEY = os.environ['CONGRESS_GOV_API_KEY']
CONGRESS_API_URL = "https://api.congress.gov/v3"


class Command(CongressArgMixin, BaseCommand):
    help = """
        Fetches congress member info from api.congress.gov and stores it in the database.
        Conflicting data will be overwritten. congress.gov does not supply LIS IDs so those will
        be missing until load-lis-ids is run.
    """

    @transaction.atomic
    def handle(self, *_args, **options):
        congress = options["congress-number"]
        concatenated_member_json = _fetch_member_list_json(congress)
        member_count = 0
        created_member_count = 0
        current_bioguide_id = None
        try:
            for member_json in concatenated_member_json:
                current_bioguide_id = member_json["bioguideId"]
                member_count += 1
                print(f"Saving member {member_count} {current_bioguide_id}", end="\r")
                member, created = Member.objects.update_or_create(
                    bioguide_id=current_bioguide_id,
                    defaults={
                        "current_party": member_json["partyName"],
                        "inverted_name": member_json["name"],
                    },
                )
                if created:
                    created_member_count += 1
                # Contiguous terms in the same chamber are grouped under one term in this API.
                # Multiple terms could indicate a mid-session switch from the House to the Senate
                # or vice versa. The easiest way to handle all edge cases is to request the
                # detailed term info for any member with multiple terms.
                if len(member_json["terms"]["item"]) == 1:
                    chamber = member_json["terms"]["item"][0]["chamber"]
                    _save_term(congress, member, chamber, member_json["state"], member_json.get("district"))
                else:
                    terms = _fetch_terms_json(congress, current_bioguide_id)
                    for term in terms:
                        _save_term(
                            congress,
                            member,
                            term["chamber"],
                            term["stateName"],
                            term.get("district"),
                        )
        except:
            print()  # Skip over carriage return to preserve last print statement.
            raise

        print(f"Saved {member_count} members, {created_member_count} new.")


def _fetch_member_list_json(congress: int) -> list[dict[str, any]]:
    url = f"{CONGRESS_API_URL}/member/congress/{congress}"
    concatenated_member_json = []
    page_count = 1
    print(f"Fetching page {page_count}", end="\r")
    members_request = requests.get(
        url, params={"API_KEY": CONGRESS_GOV_API_KEY, "format": "json", "limit": 250}
    )

    if members_request.status_code != 200:
        raise CommandError(
            f"{url} returned {members_request.status_code} status with body:\n{members_request.text}"
        )
    response_json = members_request.json()
    concatenated_member_json.extend(response_json["members"])
    try:
        next_page_url = response_json["pagination"]["next"]
    except KeyError:
        next_page_url = None
    while next_page_url is not None:
        page_count += 1
        print(f"Fetching page {page_count}", end="\r")
        members_request = requests.get(
            next_page_url,
            params={"API_KEY": CONGRESS_GOV_API_KEY, "format": "json", "limit": 250},
        )
        if members_request.status_code != 200:
            raise CommandError(
                f"{url} returned {members_request.status_code} status with body:\n{members_request.text}"
            )
        response_json: dict = members_request.json()
        concatenated_member_json.extend(response_json["members"])

        try:
            next_page_url = response_json["pagination"]["next"]
        except KeyError:
            next_page_url = None
    print(f"Fetched {len(concatenated_member_json)} members over {page_count} pages")
    return concatenated_member_json


def _fetch_terms_json(congress: int, bioguide_id: str) -> list[dict[str, any]]:
    url = f"{CONGRESS_API_URL}/member/{bioguide_id}"
    request = requests.get(
        url,
        params={"API_KEY": CONGRESS_GOV_API_KEY, "format": "json"},
    )
    if request.status_code != 200:
        raise CommandError(
            f"{url} returned {request.status_code} status with body:\n{request.text}"
        )
    terms = request.json()["member"]["terms"]
    return [term for term in terms if term["congress"] == congress]


def _save_term(
    congress: int, member: Member, chamber: dict, state: str, district: int | None = None
) -> None:
    CongressMembership.objects.update_or_create(
        chamber=Chamber.from_full_name(chamber),
        congress=congress,
        member=member,
        defaults={"state": state, "district": district},
    )
