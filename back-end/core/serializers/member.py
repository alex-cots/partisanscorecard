from rest_framework import serializers
from core.models import CongressMembership, Member, MemberStats

class MemberStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberStats
        fields = [
            "vote_count",
            "vote_with_democrats_count",
            "vote_with_republicans_count",
            "vote_with_democrats_percentage",
            "vote_with_republicans_percentage",
            "calculation_time",
            "democratic_loyalty_rank_in_chamber",
            "democratic_loyalty_rank_in_party",
            "republican_loyalty_rank_in_chamber",
            "republican_loyalty_rank_in_party",
        ]
        depth = 1


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "bioguide_id",
            "current_party",
            "inverted_name",
            "name",
            "lis_id",
        ]


class CongressMembershipListSerializer(serializers.ModelSerializer):
    member = MemberSerializer()
    memberstats = MemberStatsSerializer()

    class Meta:
        model = CongressMembership
        fields = ["chamber", "congress", "state", "district", "member", "memberstats"]
        depth = 1

    def to_representation(self, instance):
        """Override this method to bring the member and memberstats fields up to the top-level."""
        representation = super().to_representation(instance)
        member = representation.pop("member")
        for field in MemberSerializer.Meta.fields:
            representation[field] = member[field]
        memberstats = representation.pop("memberstats")
        for field in MemberStatsSerializer.Meta.fields:
            representation[field] = memberstats[field]
        return representation
