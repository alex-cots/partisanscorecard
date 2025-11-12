from django.db import models

from core.enums import Chamber

class Member(models.Model):
    bioguide_id = models.TextField(primary_key=True, help_text="Corresponds to bioguideId in api.congress.gov.")
    current_party = models.TextField()
    inverted_name = models.TextField(help_text="Inverted version of the full name, i.e. Lastname, Firstname. Should correspond to invertedOrderName in api.congress.gov.")
    lis_id = models.TextField(unique=True, null=True, blank=True, help_text="Senators have an LIS ID that is used instead of the bioguide ID when reporting vote results (unclear why).")

    @property
    def name(self):
        split_name = self.inverted_name.split(',', 2)
        split_name = [segment.strip() for segment in split_name]
        if len(split_name) == 1:
            return split_name[0]
        if len(split_name) == 2:
            return f'{split_name[1]} {split_name[0]}'
        return f'{split_name[1]} {split_name[0]} {split_name[2]}'

    def __str__(self):
        return f"{self.bioguide_id} {self.inverted_name} ({self.current_party})"

    def calculate_stats(self, save=False):
        return

class CongressMembership(models.Model):
    chamber = models.TextField(choices=Chamber)
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    congress = models.PositiveSmallIntegerField()
    state = models.TextField()
    # House-only field.
    district = models.PositiveSmallIntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['chamber', 'member', 'congress'], name='core_congressmembership_chamber_member_congress_unique')
        ]

    def __str__(self):
        return f"{self.congress} {self.member}"
