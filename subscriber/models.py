from django.db import models

class Subscriber(models.Model):
    subscriber_id = models.CharField(max_length=20, null=False)
    first_name = models.CharField(max_length=15)
    match = models.ForeignKey(to='match.Match', on_delete=models.CASCADE)

    def __str__(self):
        return self.subscriber_id