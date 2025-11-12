from abc import ABC, abstractmethod
from collections import defaultdict
from django.db.models import F, Prefetch, Q
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from core.enums import Chamber
from core.models import CongressMembership, Member, Vote
from core.serializers import CongressMembershipListSerializer, MemberDetailSerializer


class CongressMembershipListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, ABC):
    serializer_class = CongressMembershipListSerializer

    @property
    @abstractmethod
    def chamber(self):
        """This should be the chamber enum associated with this class."""

    def get_queryset(self):
        congress_number = self.kwargs["congress"]
        queryset = CongressMembership.objects.filter(
            congress=congress_number, chamber=self.chamber
        ).select_related("member", "memberstats")
        return queryset


class HouseViewSet(CongressMembershipListViewSet):
    chamber: Chamber = Chamber.HOUSE


class SenateViewSet(CongressMembershipListViewSet):
    chamber: Chamber = Chamber.SENATE


class MemberDetailViewSet(viewsets.GenericViewSet):
    serializer_class = MemberDetailSerializer

    queryset = Member.objects.prefetch_related(
        "congressmembership_set__memberstats",
        Prefetch("vote_set", Vote.objects.select_related("roll_call").order_by('-roll_call__timestamp'))
    )

    def retrieve(self, _request, *_args, **_kwargs):
        """
        Modified from RetrieveModelViewset to add nested votes.

        Might be able to move logic to serializers.
        """
        member = self.get_object()
        vote_dict = defaultdict(list)
        for vote in member.vote_set.all():
            vote_dict[vote.roll_call.congress].append(vote)
        memberships_with_votes = list(member.congressmembership_set.order_by('-congress', '-chamber'))
        for congress_membership in memberships_with_votes:
            congress_membership.vote_set = vote_dict[congress_membership.congress]
        member.memberships_with_votes = memberships_with_votes
        serializer = self.get_serializer(member)
        return Response(serializer.data)
