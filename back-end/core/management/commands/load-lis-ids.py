import os
import yaml

from django.core.management.base import BaseCommand
from django.db import transaction
from core.enums import Chamber
from core.models import Member

LEGISLATOR_PATHS = [
    f"{os.environ['CONGRESS_DATA_DIR']}/legislators-current.yaml",
    f"{os.environ['CONGRESS_DATA_DIR']}/legislators-historical.yaml",
]


class Command(BaseCommand):
    help = """
        Saves LIS IDs used to identify senators in senate vote records. Any senator records missing
        the ID will be updated. IDs are taken from open source congress data:
        https://github.com/unitedstates/congress-legislators.
    """

    @transaction.atomic
    def handle(self, *_args, **_options):
        senators_missing_ids = Member.objects.filter(
            congressmembership__chamber=Chamber.SENATE, lis_id__isnull=True
        )
        senator_dict = {senator.bioguide_id: senator for senator in senators_missing_ids}
        if len(senator_dict) == 0:
            print("No senators missing LIS IDs.")
            return

        print(f"Processing {len(senator_dict)} senators missing lis_ids.")
        for legislator_path in LEGISLATOR_PATHS:
            with open(legislator_path) as file:
                print(f"Loading {legislator_path} into pyyaml.")
                yaml_members: list = yaml.safe_load(file)
                print(f"Loaded {legislator_path}. Searching for LIS IDs.")
                _search_and_save_lis_ids(senator_dict, yaml_members, legislator_path)
                if not senator_dict:
                    return

def _search_and_save_lis_ids(senator_dict: dict, yaml_members: list, legislator_path: str) -> None:

    processed_count = 0
    yaml_member_count = 0
    for yaml_member in yaml_members:
        yaml_member_count += 1
        bioguide_id = yaml_member["id"]["bioguide"]
        if bioguide_id in senator_dict:
            try:
                senator = senator_dict[bioguide_id]
                senator.lis_id = yaml_member["id"]["lis"]
                senator.save(update_fields=["lis_id"])
            except:
                print(f"Error processing {bioguide_id} in {legislator_path}.")
                raise
            processed_count += 1
            senator_dict.pop(bioguide_id)
            if not senator_dict:
                print(
                    f"Processed {yaml_member_count} members in {os.path.basename(legislator_path)}, filled {processed_count} lis_ids, with {len(senator_dict)} still missing.",
                )
                return
    print(
        f"Processed {yaml_member_count} members in {os.path.basename(legislator_path)}, filled {processed_count} lis_ids, with {len(senator_dict)} still missing.",
    )
