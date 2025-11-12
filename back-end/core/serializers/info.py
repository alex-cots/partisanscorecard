from rest_framework import serializers

class InfoSerializer(serializers.Serializer):
    congress = serializers.IntegerField()
    chamber = serializers.CharField()
    roll_call_count = serializers.IntegerField()
    member_count = serializers.IntegerField()
    democrat_count = serializers.IntegerField()
    republican_count = serializers.IntegerField()
