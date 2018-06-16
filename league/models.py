import uuid
from django.db import models

class League(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    en_name = models.CharField(max_length=10)
    vi_name = models.CharField(max_length=10)
    country = models.ForeignKey(to='country.Country', on_delete=models.CASCADE)

    def __str__(self):
        return "{} / {}".format(self.vi_name, self.country)
