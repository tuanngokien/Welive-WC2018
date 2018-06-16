from django.db import models

class MatchStatisticEnum:
    SHOTS_ON_TARGET = {"description" : "Sút trúng đích", "type" : (1,2)}
    SHOTS_OFF_TARGET = {"description" : "Sút không trúng đích", "type" : (3,4)}
    POSSESSIONS = {"description" : "Cầm bóng (%)", "type" : (5,6)}
    OFFSIDES = {"description" : "Việt vị", "type" : (7,8)}
    FOULS = {"description" : "Phạm lỗi", "type" : (9,10)}
    YELLOW_CARDS = {"description" : "Thẻ vàng", "type" : (11,12)}
    RED_CARDS = {"description": "Thẻ đỏ", "type": (13, 14)}
    GOAL_KICKS = {"description" : "Phát bóng", "type" : (15,16)}
    CORNERS = {"description" : "Phạt góc", "type" : (17,18)}

class MatchStatistic(models.Model):
    match = models.ForeignKey(to='match.Match', on_delete=models.CASCADE)
    type = models.CharField(max_length=2)
    value = models.FloatField(default=0)