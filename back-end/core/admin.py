from django.contrib import admin
from core import models


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    readonly_fields = ["name"]
    fields = readonly_fields + [
        field.name for field in models.Member._meta.get_fields() if not field.is_relation
    ]


@admin.register(models.MemberStats)
class MemberStatsAdmin(admin.ModelAdmin):
    readonly_fields = [
        "vote_with_democrats_percentage",
        "vote_with_republicans_percentage",
        "calculation_time",
        "congress_membership",
        "vote_count",
        "vote_with_democrats_count",
        "vote_with_republicans_count",
        "democratic_loyalty_rank_in_chamber",
        "democratic_loyalty_rank_in_party",
        "republican_loyalty_rank_in_chamber",
        "republican_loyalty_rank_in_party",
    ]


admin.site.register(models.CongressMembership)
admin.site.register(models.Bill)
admin.site.register(models.RollCall)
admin.site.register(models.Vote)
