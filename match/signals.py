from django.db.models.signals import pre_save
from django.dispatch import receiver
from fbmq import Template

from .models import MatchEvent
from .helpers import get_vi_datetime_now
from webhook.views import page

@receiver([pre_save], sender = MatchEvent)
def notify_new_event(sender, instance, **kwargs):
    print("[{}] Sending new event {}".format(get_vi_datetime_now().strftime("%d/%m/%Y %H:%M:%S"), instance.event_to_notification))
    subscribers = instance.match.subscriber_set.all()
    message = Template.Generic([Template.GenericElement(title = "Bàn thắng !!! " + instance.match.scoreboard(),
                                                        subtitle= instance.event_to_notification)])
    for s in subscribers:
        page.send(s.subscriber_id, message = message)