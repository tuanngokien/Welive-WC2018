from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import MatchEvent
from webhook.views import page

@receiver([pre_save], sender = MatchEvent)
def notify_new_event(sender, instance, **kwargs):
    page.send(1635392039906890,  str(instance))