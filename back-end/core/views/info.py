from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.response import Response
from core.models import CongressMembership, RollCall
from core.enums import Chamber

class InfoViewSet(viewsets.ViewSet):
    def list(self, request):
        membership_queryset = CongressMembership.objects.values('congress').annotate(
            house_member_count=Count('pk', filter=Q(chamber=Chamber.HOUSE)),
            house_democrat_count=Count('pk', filter=Q(chamber=Chamber.HOUSE) & Q(member__current_party='Democratic')),
            house_republican_count=Count('pk', filter=Q(chamber=Chamber.HOUSE) & Q(member__current_party='Republican')),
            senate_member_count = Count('pk', filter=Q(chamber=Chamber.SENATE)),
            senate_democrat_count=Count('pk', filter=Q(chamber=Chamber.SENATE) & Q(member__current_party='Democratic')),
            senate_republican_count=Count('pk', filter=Q(chamber=Chamber.SENATE) & Q(member__current_party='Republican'))
        ).order_by('-congress')
        roll_call_queryset = RollCall.objects.values('congress').annotate(
            house_roll_call_count=Count('pk', filter=Q(chamber=Chamber.HOUSE)),
            senate_roll_call_count = Count('pk', filter=Q(chamber=Chamber.SENATE))
        ).order_by('-congress')
        data = []
        for membership_aggregation in membership_queryset:
            house_roll_call_count = 0
            senate_roll_call_count = 0
            for roll_call_aggregation in roll_call_queryset:
                if roll_call_aggregation['congress'] == membership_aggregation['congress']:
                    house_roll_call_count = roll_call_aggregation['house_roll_call_count']
                    senate_roll_call_count = roll_call_aggregation['senate_roll_call_count']
            data.append({
                'congress': membership_aggregation['congress'],
                'chamber': Chamber.HOUSE,
                'member_count': membership_aggregation['house_member_count'],
                'democrat_count': membership_aggregation['house_democrat_count'],
                'republican_count': membership_aggregation['house_republican_count'],
                'roll_call_count': house_roll_call_count
            })

            data.append({
                'congress': membership_aggregation['congress'],
                'chamber': Chamber.SENATE,
                'member_count': membership_aggregation['senate_member_count'],
                'democrat_count': membership_aggregation['senate_democrat_count'],
                'republican_count': membership_aggregation['senate_republican_count'],
                'roll_call_count': senate_roll_call_count
            })
        return Response(data)
