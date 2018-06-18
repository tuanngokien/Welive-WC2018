from django.db.models.signals import pre_save
from django.dispatch import receiver
from fbmq import Template

from .models import MatchEvent
from webhook.views import page

@receiver([pre_save], sender = MatchEvent)
def notify_new_event(sender, instance, **kwargs):
    subscribers = instance.match.subscriber_set.all()
    for s in subscribers:
        page.send(s.subscriber_id,
                  Template.Generic([Template.GenericElement(title = "Bàn thắng !!! " + instance.match.scoreboard(),
                                                            subtitle= instance.event_to_notification,
                                                            buttons = [
                                                                Template.ButtonPostBack("Xem video","TEST"),
                                                            ]
                                                            )]))