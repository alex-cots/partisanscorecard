from typing import Self
from django.db import models

from core.enums import Chamber
from .member import Member


class RollCall(models.Model):
    bill = models.ForeignKey("Bill", on_delete=models.CASCADE, blank=True, null=True)
    category = models.TextField()
    chamber = models.TextField(choices=Chamber)
    congress = models.PositiveSmallIntegerField()
    id = models.TextField(primary_key=True)
    number = models.PositiveSmallIntegerField()
    question = models.TextField()
    result = models.TextField()
    timestamp = models.DateTimeField()

    # Stats
    dem_maj_position = models.TextField(default="", db_default="")
    repub_maj_position = models.TextField(default="", db_default="")

    def calculate_majority_positions(self, save=False):
        dem_counts = dict()
        repub_counts = dict()
        votes = self.vote_set.select_related("member")
        for vote in votes:
            if vote.member.current_party == "Democratic":
                current_dem_count = dem_counts.get(vote.position, 0)
                dem_counts[vote.position] = current_dem_count + 1
            elif vote.member.current_party == "Republican":
                current_repub_count = repub_counts.get(vote.position, 0)
                repub_counts[vote.position] = current_repub_count + 1
        sort_key = lambda pair: pair[1]
        dem_count_list = [(key, value) for key, value in dem_counts.items()]
        dem_count_list.sort(key=sort_key, reverse=True)
        repub_count_list = [(key, value) for key, value in repub_counts.items()]
        repub_count_list.sort(key=sort_key, reverse=True)
        if len(dem_count_list) == 1:
            self.dem_maj_position = dem_count_list[0][0]
        else:
            if dem_count_list[0][1] == dem_count_list[1][1]:
                self.dem_maj_position = "Divided"
            else:
                self.dem_maj_position = dem_count_list[0][0]

        if len(repub_count_list) == 1:
            self.repub_maj_position = repub_count_list[0][0]
        else:
            if dem_count_list[0][1] == repub_count_list[1][1]:
                self.repub_maj_position = "Divided"
            else:
                self.repub_maj_position = repub_count_list[0][0]

        if save:
            self.save()


class VoteManager(models.Manager):
    def select_outliers(self, member: Member) -> Self:
        """Exclude votes where the member voted with their party majority."""
        queryset = self.filter(member=member)
        if member.current_party == "Democratic":
            queryset = queryset.exclude(roll_call__dem_maj_position=models.F("position"))
        elif member.current_party == "Republican":
            queryset = queryset.exclude(roll_call__repub_maj_position=models.F("position"))
        else:
            # Independents and 3rd parties are not supported.
            return self.none()
        return queryset


class Vote(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    position = models.TextField()
    roll_call = models.ForeignKey("RollCall", on_delete=models.CASCADE)

    objects = VoteManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["member", "roll_call"], name="core_vote_member_rollcall_unique"
            )
        ]

    def __str__(self):
        return f"{self.member} {self.position}"


class Bill(models.Model):
    congress = models.PositiveSmallIntegerField()
    # Rarely, the data source does not provide a title.
    title = models.TextField(blank=True)
    type = models.TextField()
    number = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["congress", "type", "number"], name="core_bill_congress_number_unique"
            )
        ]
