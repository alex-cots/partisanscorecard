from rest_framework import viewsets

from core.enums import Chamber
from core.models import RollCall
from core.serializers import RollCallSerializer

class HouseRollCallViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RollCallSerializer

    def get_queryset(self):
        congress_number = self.kwargs['congress']
        queryset = RollCall.objects.filter(chamber=Chamber.HOUSE, congress=congress_number)
        member_id = self.request.query_params.get('member_id')
        if member_id is not None:
            queryset = queryset.filter(vote__member_id=member_id)
        return queryset.order_by('-timestamp')

class SenateRollCallViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RollCallSerializer

    def get_queryset(self):
        congress_number = self.kwargs['congress']
        queryset = RollCall.objects.filter(chamber=Chamber.SENATE, congress=congress_number)
        member_id = self.request.query_params.get('member_id')
        if member_id is not None:
            queryset = queryset.filter(vote__member_id=member_id)
        return queryset.order_by('-timestamp')
