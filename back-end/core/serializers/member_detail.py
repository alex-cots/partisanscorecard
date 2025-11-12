from rest_framework import serializers

from core.models.member import CongressMembership, Member
from .member import MemberStatsSerializer
from .vote import VoteWithRollCallSerializer


class CongressMembershipWithVotesSerializer(serializers.ModelSerializer):
    vote_set = VoteWithRollCallSerializer(many=True)
    memberstats = MemberStatsSerializer()

    class Meta:
        model = CongressMembership
        fields = [
            "chamber",
            "congress",
            "district",
            "memberstats",
            "vote_set",
            "state",
        ]
        depth = 1

    def to_representation(self, instance):
        """Override this method to bring the memberstats fields up to the top-level."""
        representation = super().to_representation(instance)
        memberstats = representation.pop("memberstats")
        if memberstats is not None:
            for field in MemberStatsSerializer.Meta.fields:
                representation[field] = memberstats[field]
        return representation

class MemberDetailSerializer(serializers.ModelSerializer):
    congresses_served = CongressMembershipWithVotesSerializer(source="memberships_with_votes", many=True)

    class Meta:
        model = Member
        fields = ["bioguide_id", "current_party", "inverted_name", "name", "lis_id", "congresses_served"]
