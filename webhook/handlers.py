from fbmq import Template, QuickReply
import re
from django.utils import timezone

from .views import page
from match.models import Match
from subscriber.models import Subscriber

@page.handle_postback
def postback(event):
    pass

@page.callback(["SUBSCRIBE_MATCH_\d+"])
def handle_subscribe_match(action, event):
    match_id = re.search('_([0-9]+)$', action).group(1)
    match = Match.objects.get(id = match_id)
    first_name = page.get_user_profile(event.sender_id).get("first_name", "Anonymous")
    subcriber, created = Subscriber.objects.get_or_create(subscriber_id = event.sender_id, first_name = first_name, match_id = match_id)
    if created:
        message = "Đăng ký theo dõi trận {} thành công ️🏆️🏆️🏆".format(match.scoreboard(score_included=False))
        page.send(event.sender_id, message)

@page.callback(["UNSUBSCRIBE_MATCH_\d+"])
def handle_unsubscribe_match(action, event):
    match_id = re.search('_([0-9]+)$', action).group(1)
    match = Match.objects.get(id = match_id)
    try:
        subcriber = Subscriber.objects.get(subscriber_id = event.sender_id, match_id = match_id)
    except Subscriber.DoesNotExist:
        return
    else:
        subcriber.delete()
        message = "Bỏ theo dõi trận {} thành công :D".format(match.scoreboard())
        page.send(event.sender_id, message)


@page.callback(['MENU_(.+)'])
def click_persistent_menu(action, event):
    MenuAction.dispatch(action, event.sender_id)

def matches_to_message(matches, recipient_id):
    message = []
    for match in matches:
        match_started = match.is_started
        title = str(match)
        if not match.subscriber_set.filter(subscriber_id=recipient_id).exists():
            subscribe_btn_title = "Theo dõi"
            subscribe_btn_payload = "SUBSCRIBE_MATCH_{}"
            subtitle = "Chọn nút \"Theo dõi\" để nhận cập nhật kết quả" if not match_started else match.statistics()
        else:
            subscribe_btn_title = "Bỏ theo dõi"
            subscribe_btn_payload = "UNSUBSCRIBE_MATCH_{}"
            subtitle = "Bạn đang theo dõi trận đấu này" if not match_started else match.statistics()

        subscribe_btn = Template.ButtonPostBack(subscribe_btn_title, subscribe_btn_payload.format(match.id))
        message.append(Template.GenericElement(title=title,
                                               subtitle=subtitle,
                                               buttons=[
                                                   subscribe_btn,
                                               ] if not match.is_ended else None))
    return Template.Generic(message)

class MenuAction:
    LIVE = "MENU_LIVE"
    SCHEDULE = "MENU_SCHEDULE"
    STANDING = "MENU_STANDING"
    NEWS = "MENU_NEWS"

    @classmethod
    def dispatch(cls, action, recipient_id):
        message = ''
        quick_replies = None
        if action.startswith(MenuAction.SCHEDULE):
            date = re.search('_([A-Z]+)$', action).group(1)
            message, quick_replies = cls.show_schedule(date, recipient_id)
        elif action == MenuAction.LIVE:
            message = cls.show_live(recipient_id)
        page.send(recipient_id = recipient_id, message = message, quick_replies = quick_replies)

    @staticmethod
    def show_live(recipient_id):
        matches = Match.objects.live()
        if len(matches) > 0:
            message = matches_to_message(matches, recipient_id)
        else:
            message = "Không có trận đấu nào đang diễn ra 😞"
        return message

    @staticmethod
    def show_schedule(date, recipient_id):
        matches = Match.objects.all()
        title = ''
        if date == "YESTERDAY":
            matches = matches.yesterday()
        elif date == "TOMOROW":
            matches = matches.tomorow()
        elif date.isdigit():
            pass
        else:
            matches = matches.today()
        message = matches_to_message(matches, recipient_id)
        quick_replies = [
            QuickReply(title="Hôm qua", payload=MenuAction.SCHEDULE + "_YESTERDAY"),
            QuickReply(title="Hôm nay ", payload=MenuAction.SCHEDULE + "_TODAY"),
            QuickReply(title="Ngày mai ", payload=MenuAction.SCHEDULE + "_TOMOROW"),
        ]
        return (message, quick_replies)

    @staticmethod
    def show_standing(*args, **kwargs):
        print("Standing")

    @staticmethod
    def show_news():
        print("News")

page.show_persistent_menu([Template.ButtonPostBack('Trực tiếp', MenuAction.LIVE),
                           Template.ButtonPostBack('Lịch thi đấu - Kết quả', MenuAction.SCHEDULE + "_TODAY"),
                           Template.ButtonPostBack('Bảng xếp hạng', MenuAction.STANDING)])