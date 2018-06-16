from django.contrib import admin

from .models import Match, MatchEvent, MatchStatistic

admin.site.register(Match)
admin.site.register(MatchEvent)
admin.site.register(MatchStatistic)

