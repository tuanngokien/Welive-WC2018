from fbmq import Page, Template
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


ACCESS_TOKEN = os.environ["FB_ACCESS_TOKEN"]
SECRET_KEY = os.environ["FB_SECRET_KEY"]

page = Page(ACCESS_TOKEN)

page.show_starting_button("GETTING_STARTED")

@page.callback(['GETTING_STARTED'])
def start_callback(payload, event):
    first_name = page.get_user_profile(event.sender_id).get("first_name", "Anonymous")
    page.send(event.sender_id, "Chào {}, vui lòng chọn các chức năng của bot trong MENU nhé !".format(first_name))

@csrf_exempt
def fb_webhook(request):
    if request.method == "GET":
        if SECRET_KEY == request.GET.get('hub.verify_token'):
            return HttpResponse(request.GET.get("hub.challenge"))
    else:
        page.handle_webhook(request.body)
    return HttpResponse("")


@page.handle_message
def message_handler(event):
    if not event.quick_reply:
        page.send(event.sender_id, "Vui lòng chọn chức năng trong phần Menu nhé 😅")
