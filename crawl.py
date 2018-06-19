import time
from datetime import datetime

from crawler import crawl_wc_2018_live_matches, crawl_wc_2018_matches
from match.models import Match
from match.helpers import get_vi_datetime_now

live_match_count = crawl_wc_2018_live_matches()
print("Start crawl, {} matches is living".format(live_match_count))

while True:
    datetime_now = get_vi_datetime_now().replace(tzinfo=None)
    if live_match_count == 0:
        match = Match.objects.coming_match()
        coming_match_datetime = datetime.combine(match.date, match.time)
        timedelta = coming_match_datetime - datetime_now
        print("Wait {} to match {}".format(timedelta, match.scoreboard(score_included=False)))
        wait_time = timedelta.total_seconds()
        time.sleep(wait_time)
        while live_match_count == 0:
            live_match_count = crawl_wc_2018_live_matches(date=datetime_now.date())
            time.sleep(10)
    while True:
        if live_match_count == 0:
            break
        curr_live_match_count = crawl_wc_2018_live_matches(date = datetime_now.date())
        if live_match_count > curr_live_match_count:
            crawl_wc_2018_matches()
        live_match_count = curr_live_match_count




