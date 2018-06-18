from django.db import models
from django.db.models import Q
from django.utils import timezone

from ..helpers import add_day, get_vi_datetime_now, get_vi_today_date
from .event import MatchEvent, TeamSide

MATCH_STATUS = {
    '' : 'Chưa bắt đầu',
    'FT' : 'Hết giờ',
    'HT' : 'Hết hiệp 1',
    'n' : 'Đang thi đấu',
}

class MatchQuerySet(models.QuerySet):
    def filter_date(self, date):
        return self.filter(
            (Q(date = date) & Q(time__gte = "6:00:00")) |
            (Q(date = add_day(date, 1)) & Q(time__lte = "6:00:00"))
        ).select_related("hometeam", "awayteam")

    def today(self):
        today_date = get_vi_today_date()
        return self.filter_date(today_date)

    def tomorow(self):
        today_date = get_vi_today_date()
        return self.filter_date(add_day(today_date, 1))

    def yesterday(self):
        today_date = get_vi_today_date()
        return self.filter_date(add_day(today_date, -1))

    def just_ended_match(self):
        datetime_now = get_vi_datetime_now()
        return self.filter(date__lte=datetime_now.date(), status='FT').order_by("-date", "-time").first()

    def coming_match(self):
        datetime_now = get_vi_datetime_now()
        return self.filter(date__gte = datetime_now.date(), status = '').first()

    def live(self):
        return self.filter(~Q(status = 'FT') & ~Q(status = ''))

class Match(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    league = models.ForeignKey(to='league.League', on_delete=models.CASCADE)
    hometeam = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name="home_matches")
    hometeam_score = models.IntegerField(default=-1)
    awayteam = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name="away_matches")
    awayteam_score = models.IntegerField(default=-1)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=8, null=False, blank=True, default='')

    objects = MatchQuerySet.as_manager()

    class Meta:
        ordering = ("date", "time")

    @property
    def is_started(self):
        return self.status != ''

    @property
    def is_ended(self):
        return self.status == "FT"

    def __str__(self):
        if self.is_ended:
            return "💠 {} {} - {} {}".format(self.hometeam, self.hometeam_score, self.awayteam_score, self.awayteam)
        else:
            is_playing = self.is_started and not self.is_ended
            if is_playing:
                status = "🔴{} | ".format(self.status)
                return status + self.scoreboard()
            else:
                return "🔘 {} {} | {} - {}".format(self.time.strftime("%H:%M"), self.date.strftime("%d/%m"), self.hometeam.vi_name, self.awayteam.vi_name)

    def scoreboard(self, score_included = True):
        return "{} {}-{} {}".format(self.hometeam.vi_name,
                                      str(self.hometeam_score) + ' ' if self.is_started and score_included else '',
                                      ' ' + str(self.awayteam_score) if self.is_started and score_included else '',
                                      self.awayteam.vi_name)

    def statistics(self):
        hometeam_stat = []
        awayteam_stat = []
        goal_events = MatchEvent.objects.goal_events(match_id = self.id)
        for e in goal_events:
            event_alias = e.get_event_alias()
            if event_alias["side"] == TeamSide.HOME:
                hometeam_stat.append(e.detail)
            else:
                awayteam_stat.append(e.detail)
        str_stat = ''
        if len(hometeam_stat) > 0:
            str_stat += "{}: {}\n".format(self.hometeam, ', '.join(hometeam_stat))
        if len(awayteam_stat) > 0:
            str_stat += "{}: {}".format(self.awayteam, ', '.join(awayteam_stat))
        return str_stat