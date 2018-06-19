import os, json, requests, logging,re
from django.utils import timezone

from .helpers import convert_time_zone
from match.helpers import  add_day, str_to_date, date_to_str, get_vi_datetime_now
from match.models import Match, TeamSide, MatchEventEnum, MatchEvent, MatchStatistic
from team.models import Team
from country.models import Country
from league.models import League

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BASE_API = "https://apifootball.com/api/"
API_KEY = os.environ["API_KEY"]

class MatchCrawler:
    BASE_TIME_ZONE = 'Europe/Monaco'
    VI_TIME_ZONE = 'Asia/Ho_Chi_Minh'


    MATCH_API = BASE_API + "?action=get_events"

    def __init__(self, match_id, league_id, country_id, from_date, to_date, live = False):
        self.match_id = match_id
        self.league_id = league_id
        self.country_id = country_id
        self.live = live
        self.from_date = from_date
        self.to_date = to_date
        self.match_count = 0
        self.match_infos = []
        self.match_events = []

    def crawl_to_db(self):
        logger.info('Crawling {}'.format(self.MATCH_API))
        r = requests.get(url = self.MATCH_API,
                      params = {"from" : self.from_date,
                                "to" : self.to_date,
                                "match_id" : self.match_id,
                                "league_id" : self.league_id,
                                "country_id" : self.country_id,
                                "match_live" : 1 if self.live else 0,
                                "APIkey" : API_KEY}
                      )
        if "error" in r.text:
            return 0
        self.parse_data(r.text)
        self.save_to_db()
        return self.match_count

    def parse_data(self, response):
        logger.info('Parsing data')
        data = json.loads(response)
        parsed_data = []
        for match in data:
            self.match_count += 1
            self.parse_match_info(match)
            if match.get("match_status", "") != "":
                self.parse_goal_event(match)

    def parse_match_info(self, match):
        hometeam = Team.objects.get(en_name=match.get("match_hometeam_name"))
        hometeam_score = match.get("match_hometeam_score")
        hometeam_score = hometeam_score if hometeam_score not in ("", "?") else -1
        awayteam = Team.objects.get(en_name=match.get("match_awayteam_name"))
        awayteam_score = match.get("match_awayteam_score")
        awayteam_score = awayteam_score if awayteam_score not in ("", "?") else -1
        time, date = convert_time_zone(match.get("match_time") + ":00",
                                       match.get("match_date"),
                                       MatchCrawler.BASE_TIME_ZONE,
                                       MatchCrawler.VI_TIME_ZONE)
        self.match_infos.append({"id": match.get("match_id"),
                            "league_id": match.get("league_id"),
                            "hometeam": hometeam,
                            "hometeam_score": hometeam_score,
                            "awayteam": awayteam,
                            "awayteam_score": awayteam_score,
                            "date": date,
                            "time": time,
                            "status": match.get("match_status")})

    def parse_goal_event(self, match):
        match_id = match.get("match_id")
        goal_events = match.get("goalscorer")
        curr_goal_event_count = len(goal_events)
        saved_goal_event_count = MatchEvent.objects.goal_events(match_id).count()
        if saved_goal_event_count < curr_goal_event_count:
            unsaved_goal_events = goal_events[saved_goal_event_count:]
            for event in unsaved_goal_events:
                scorer_side = "home_scorer"
                scorer = event.get(scorer_side, "")
                side = TeamSide.HOME
                if scorer == "":
                    side = TeamSide.AWAY
                    scorer_side = "away_scorer"
                    scorer = event.get(scorer_side, "")
                event_type = MatchEventEnum.SCORE["side"][side]

                if self.live:
                    # avoid create event like failed penalty goal (API still provide)
                    if side == TeamSide.HOME:
                        curr_side_score = int(match.get("match_hometeam_score"))
                    else:
                        curr_side_score = int(match.get("match_awayteam_score"))
                    if len([e for e in goal_events if e.get(scorer_side, "") != ""]) > curr_side_score:
                        continue
                self.match_events.append({
                    "match_id" : match_id,
                    "event_type" : event_type,
                    "time" : event.get("time", 0),
                    "player_name" : re.sub("^.*[.] ", '', scorer)})

    def save_to_db(self):
        logger.info("Saving matches to database")
        for match in self.match_infos:
            id = match.pop("id")
            saved_match = Match.objects.update_or_create(id = id, defaults=match)

        for event in self.match_events:
            saved_event = MatchEvent.objects.create(**event)

        return True


def crawl_wc_2018_matches():
    datetime_now = str(get_vi_datetime_now().date())
    from_date = add_day(datetime_now, -1)
    to_date = add_day(datetime_now, 1)
    wc_league = Country.objects.get(en_name="World Cup 2018")
    wc_groups = League.objects.filter(country=wc_league)
    for group in wc_groups:
        crawler = MatchCrawler(None, group.id, wc_league.id, from_date, to_date)
        crawler.crawl_to_db()

def crawl_wc_2018_live_matches(date = get_vi_datetime_now().date()):
    from_date = add_day(date, -1)
    to_date = add_day(date, 1)
    wc_league = Country.objects.get(en_name="World Cup 2018")
    crawler = MatchCrawler(None, None, wc_league.id, from_date, to_date, live = True)
    live_match_count = crawler.crawl_to_db()
    return live_match_count

if __name__ == "__main__":
    crawl_wc_2018_matches()