from django.db import models

class TeamSide:
    HOME = 0
    AWAY = 1

class MatchEventEnum:
    SCORE = {"description" : "Bàn thắng", "type" : (1,2)} # TYPE(HOME, AWAY)
    YELLOW_CARD = {"description" : "Thẻ vàng", "type" : (3,4)}
    RED_CARD = {"description" : "Thẻ đỏ", "type" : (5,6)}
    SUBSTITUTE = {"description" : "Thay người", "type" : (7,8)}

    @classmethod
    def _get_event_description(cls, event_type):
        for e in vars(cls):
            e_ref = getattr(cls, e)
            if not e.startswith("_") and int(event_type) in e_ref["type"]:
                return e_ref["description"]
        return "Unknown"

class MatchEvent(models.Model):
    match = models.ForeignKey(to='match.Match', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=15)
    time = models.CharField(max_length=8)
    player_name = models.TextField()

    def __str__(self):
        event_name =  MatchEventEnum._get_event_description(self.event_type)
        return "{} \n{} {}".format(self.match.scoreboard(), self.time, self.player_name)
