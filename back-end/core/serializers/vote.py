from rest_framework import serializers
from core.models import RollCall, Vote
from core.serializers.member import MemberSerializer

class VoteWithMemberSerializer(serializers.ModelSerializer):
    member = MemberSerializer()

    class Meta:
        model = Vote
        fields = ['position', 'member']

class BaseRollCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = RollCall
        fields = '__all__'


class RollCallSerializer(BaseRollCallSerializer):
    votes = VoteWithMemberSerializer(many=True, source='vote_set')

    class Meta(BaseRollCallSerializer.Meta):
        pass

class VoteWithRollCallSerializer(serializers.ModelSerializer):
    roll_call = BaseRollCallSerializer()

    class Meta:
        model = Vote
        fields = ['position', 'roll_call']
