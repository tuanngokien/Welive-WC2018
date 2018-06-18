from django.db import models

class TeamSide:
    HOME = 0
    AWAY = 1

class MatchEventEnum:
    SCORE = {"description" : "vừa lập công cho", "side" : (1,2)} # TYPE(HOME, AWAY)
    YELLOW_CARD = {"description" : "Thẻ vàng", "side" : (3,4)}
    RED_CARD = {"description" : "Thẻ đỏ", "side" : (5,6)}
    SUBSTITUTE = {"description" : "Thay người", "side" : (7,8)}

    @classmethod
    def _get_event(cls, event_type):
        for e in vars(cls):
            e_ref = getattr(cls, e)
            if not e.startswith("_") and event_type in e_ref["side"]:
                return e_ref
        return "Unknown"

class MatchEventQueryset(models.QuerySet):
    def goal_events(self, match_id):
        return self.filter(match_id=match_id,
               event_type__in=(MatchEventEnum.SCORE["side"][TeamSide.HOME], MatchEventEnum.SCORE["side"][TeamSide.AWAY]))

class MatchEvent(models.Model):
    match = models.ForeignKey(to='match.Match', on_delete=models.CASCADE)
    event_type = models.PositiveIntegerField()
    time = models.CharField(max_length=8)
    player_name = models.TextField()

    objects = MatchEventQueryset.as_manager()

    class Meta:
        ordering = ("match", "time")

    def __str__(self):
        return "{} \n{} {}".format(self.match.scoreboard(), self.time, self.player_name)

    def get_event_alias(self):
        event = MatchEventEnum._get_event(self.event_type)
        side = event["side"].index(self.event_type)
        descr = event["description"]
        return {"side" : side, "description" : descr}

    @property
    def event_to_notification(self):
        event = self.get_event_alias()
        side = event["side"]
        if side == TeamSide.HOME:
            team_name = str(self.match.hometeam)
        else:
            team_name = str(self.match.awayteam)
        return "{} {} {} ({})".format(self.player_name, event["description"], team_name, self.time)

    @property
    def detail(self):
        return "{} {}".format(self.player_name, self.time)