from django.db import models
from django.utils import timezone
from django.db.models import Q

from ..helpers import add_day

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
        )

    def today(self):
        today_date = timezone.localtime().date()
        return self.filter_date(today_date)

class Match(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    league = models.ForeignKey(to='league.League', on_delete=models.CASCADE)
    hometeam = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name="home_matches")
    hometeam_score = models.IntegerField(default=-1)
    awayteam = models.ForeignKey(to='team.Team', on_delete=models.CASCADE, related_name="away_matches")
    awayteam_score = models.IntegerField(default=-1)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=8)

    objects = MatchQuerySet.as_manager()

    class Meta:
        ordering = ("date", "time")

    def __str__(self):
        return "{} | {} - {}".format(self.time.strftime("%H:%M"), self.hometeam.vi_name, self.awayteam.vi_name)

    def scoreboard(self):
        return "{} {} - {} {}".format(self.hometeam.vi_name, self.hometeam_score, self.awayteam_score, self.awayteam.vi_name)