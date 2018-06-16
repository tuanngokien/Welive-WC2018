from fbmq import Page
import os
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from match.helpers import add_day
from match.models import Match

ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
SECRET_KEY = os.environ["SECRET_KEY"]

page = Page(ACCESS_TOKEN)

@csrf_exempt
def fb_webhook(request):
    if request.method == "GET":
        return HttpResponse(request.GET.get("hub.challenge"))
    else:
        page.handle_webhook(request.body)
    return HttpResponse("")


@page.handle_message
def message_handler(event):
    """:type event: fbmq.Event"""
    sender_id = event.sender_id
    message = event.message_text
    date = timezone.localtime().date()
    if message == "tomorow":
        date = add_day(date , 1)
    elif message == "yesterday":
        date = add_day(date, -1)
    matches = '\n'.join([str(match) for match in Match.objects.filter_date(date)])
    print(sender_id)
    page.send(sender_id, matches)
    return HttpResponse("")

    # print(request)
    # if request.method == "GET":
    #     verify_token = request.GET.get('hub.verify_token')
    #     if SECRET_KEY == verify_token:
    #         return HttpResponse(request.GET.get('hub.challenge'))
    # else:
    #     print(request.body)
