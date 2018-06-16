from django.db import models

class Team(models.Model):
    league = models.ForeignKey(to="league.League", on_delete=models.CASCADE)
    en_name = models.CharField(max_length=30)
    vi_name = models.CharField(max_length=30)

    def __str__(self):
        return self.vi_name