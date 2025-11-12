from datetime import datetime, timezone
from typing import Literal

from django.db import models

from core.enums import Chamber
from .vote import Vote
from .member import CongressMembership

type PercentageField = Literal[
    "vote_with_democrats_percentage", "vote_with_republicans_percentage"
]

type RankField = Literal[
    "democratic_loyalty_rank_in_chamber",
    "democratic_loyalty_rank_in_party",
    "republican_loyalty_rank_in_chamber",
    "republican_loyalty_rank_in_party",
]


class MemberStatsManager(models.Manager):
    @staticmethod
    def _calculate_loyalty_ranks_helper(
        sorted_queryset: list["MemberStats"],
        percentage_field: PercentageField,
        rank_field: RankField,
    ):
        rank = 1
        prev_percentage = 200
        prev_rank = 1
        for cur_stats in sorted_queryset:
            cur_percentage = getattr(cur_stats, percentage_field)
            # Reflect ties in ranking.
            if prev_percentage == cur_percentage:
                setattr(cur_stats, rank_field, prev_rank)
            else:
                setattr(cur_stats, rank_field, rank)
                prev_rank = rank

            rank += 1
            prev_percentage = cur_percentage
            cur_stats.save(update_fields=[rank_field])

    def calculate_loyalty_ranks(self, congress: int):
        # Fetch each appropriate queryset, then sort and rank them in Python.
        # Doing the sorting in Python because calculating the percentages in SQL is weirdly difficult using Django.
        qs_by_congress = self.filter(congress_membership__congress=congress)
        senate_qs = qs_by_congress.filter(congress_membership__chamber=Chamber.SENATE)
        house_qs = qs_by_congress.filter(congress_membership__chamber=Chamber.HOUSE)

        def democratic_key_fn(stats):
            return stats.vote_with_democrats_percentage

        def republican_key_function(stats):
            return stats.vote_with_republicans_percentage

        # Senate chamber democratic loyalty
        sorted_stats_list = sorted(senate_qs.all(), key=democratic_key_fn, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_democrats_percentage",
            "democratic_loyalty_rank_in_chamber",
        )

        # Senate chamber republican loyalty
        sorted_stats_list = sorted(senate_qs.all(), key=republican_key_function, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_republicans_percentage",
            "republican_loyalty_rank_in_chamber",
        )

        # House chamber democratic loyalty
        sorted_stats_list = sorted(house_qs.all(), key=democratic_key_fn, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_democrats_percentage",
            "democratic_loyalty_rank_in_chamber",
        )

        # House chamber republican loyalty
        sorted_stats_list = sorted(house_qs.all(), key=republican_key_function, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_republicans_percentage",
            "republican_loyalty_rank_in_chamber",
        )

        dem_senate_qs = senate_qs.filter(congress_membership__member__current_party="Democratic")

        # Senate democrats democratic loyalty
        sorted_stats_list = sorted(dem_senate_qs.all(), key=democratic_key_fn, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_democrats_percentage",
            "democratic_loyalty_rank_in_party",
        )

        # Senate democrats republican loyalty
        sorted_stats_list = sorted(dem_senate_qs.all(), key=republican_key_function, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_republicans_percentage",
            "republican_loyalty_rank_in_party",
        )

        dem_house_qs = house_qs.filter(congress_membership__member__current_party="Democratic")

        # House democrats democratic loyalty
        sorted_stats_list = sorted(dem_house_qs.all(), key=democratic_key_fn, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_democrats_percentage",
            "democratic_loyalty_rank_in_party",
        )

        # House democrats republican loyalty
        sorted_stats_list = sorted(dem_house_qs.all(), key=republican_key_function, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_republicans_percentage",
            "republican_loyalty_rank_in_party",
        )

        repub_senate_qs = senate_qs.filter(congress_membership__member__current_party="Republican")

        # Senate republicans republican loyalty
        sorted_stats_list = sorted(
            repub_senate_qs.all(), key=republican_key_function, reverse=True
        )
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_republicans_percentage",
            "republican_loyalty_rank_in_party",
        )

        # Senate republicans democratic loyalty
        sorted_stats_list = sorted(
            repub_senate_qs.all(), key=democratic_key_fn, reverse=True
        )
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_democrats_percentage",
            "democratic_loyalty_rank_in_party",
        )

        repub_house_qs = house_qs.filter(congress_membership__member__current_party="Republican")

        # House republicans republican loyalty
        sorted_stats_list = sorted(repub_house_qs.all(), key=republican_key_function, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_republicans_percentage",
            "republican_loyalty_rank_in_party",
        )

        # House republicans democratic loyalty
        sorted_stats_list = sorted(repub_house_qs.all(), key=democratic_key_fn, reverse=True)
        self._calculate_loyalty_ranks_helper(
            sorted_stats_list,
            "vote_with_democrats_percentage",
            "democratic_loyalty_rank_in_party",
        )


class MemberStats(models.Model):
    calculation_time = models.DateTimeField(db_default=models.functions.Now())
    congress_membership = models.OneToOneField("CongressMembership", models.CASCADE, unique=True)
    vote_count = models.IntegerField(default=0, db_default=0)
    vote_with_democrats_count = models.IntegerField(default=0, db_default=0)
    vote_with_republicans_count = models.IntegerField(default=0, db_default=0)

    democratic_loyalty_rank_in_chamber = models.PositiveSmallIntegerField(
        null=True, default=None, db_default=None
    )
    democratic_loyalty_rank_in_party = models.PositiveSmallIntegerField(
        null=True, default=None, db_default=None
    )
    republican_loyalty_rank_in_chamber = models.PositiveSmallIntegerField(
        null=True, default=None, db_default=None
    )
    republican_loyalty_rank_in_party = models.PositiveSmallIntegerField(
        null=True, default=None, db_default=None
    )

    objects = MemberStatsManager()

    @property
    def vote_with_democrats_percentage(self):
        if self.vote_count:
            return self.vote_with_democrats_count / self.vote_count
        return 0

    @property
    def vote_with_republicans_percentage(self):
        if self.vote_count:
            return self.vote_with_republicans_count / self.vote_count
        return 0

    def __str__(self):
        return f"{self.congress_membership.congress} {self.congress_membership.member_id}"

    def create_from_congress_membership(congress_membership: CongressMembership, upsert=False):
        calculation_time = datetime.now(timezone.utc)
        if upsert:
            stats, _created = MemberStats.objects.update_or_create(
                congress_membership=congress_membership,
                defaults={
                    "vote_count": 0,
                    "vote_with_democrats_count": 0,
                    "vote_with_republicans_count": 0,
                    "calculation_time": calculation_time,
                },
            )
        else:
            stats = MemberStats(
                congress_membership=congress_membership, calculation_time=calculation_time
            )
        votes = Vote.objects.filter(
            member_id=congress_membership.member_id,
            roll_call__congress=congress_membership.congress,
            roll_call__chamber=congress_membership.chamber,
        ).select_related("roll_call")

        for vote in votes:
            stats.vote_count = stats.vote_count + 1
            if vote.position == vote.roll_call.dem_maj_position:
                stats.vote_with_democrats_count += 1
            if vote.position == vote.roll_call.repub_maj_position:
                stats.vote_with_republicans_count += 1
        if upsert:
            stats.save()
        return stats
