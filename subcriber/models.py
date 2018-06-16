from django.db import models

class Subcriber(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True, null=False)
    first_name = models.CharField(max_length=15)
    match = models.ForeignKey(to='match.Match', on_delete=models.CASCADE)

    def __str__(self):
        return self.id