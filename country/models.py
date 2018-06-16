from django.db import models

class Country(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    en_name = models.CharField(max_length=30)
    vi_name = models.CharField(max_length=30)

    def __str__(self):
        return self.vi_name
