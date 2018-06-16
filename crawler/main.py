import os, json, requests, logging,re

from .helpers import convert_time_zone
from match.helpers import  add_day, str_to_date, date_to_str
from match.models import Match, TeamSide, MatchEventEnum, MatchEvent, MatchStatistic
from team.models import Team
from country.models import Country
from league.models import League

logger = logging.getLogger(__name__)
BASE_API = "https://apifootball.com/api/"
API_KEY = os.environ["API_KEY"]

class MatchCrawler:
    BASE_TIME_ZONE = 'Europe/Monaco'
    VI_TIME_ZONE = 'Asia/Ho_Chi_Minh'


    MATCH_API = BASE_API + "?action=get_events"

    def __init__(self, league_id, from_date, to_date, live = False):
        self.league_id = league_id
        self.live = live
        self.from_date = date_to_str(add_day(str_to_date(from_date), -1))
        self.to_date = date_to_str(add_day(str_to_date(to_date), 1))

    def crawl(self):
        logger.info('Crawling {}'.format(self.MATCH_API))
        r = requests.get(url = self.MATCH_API,
                      params = {"from" : self.from_date,
                                "to" : self.to_date,
                                "league_id" : self.league_id,
                                "match_live" : 1 if self.live else 0,
                                "APIkey" : API_KEY}
                      )
        self.match_infos = []
        self.match_events = []
        if "error" in r.text:
            return
        self.parse_data(r.text)

    def parse_data(self, response):
        logger.info('Parsing data')
        data = json.loads(response)
        parsed_data = []
        for match in data:
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
        saved_goal_event_count = MatchEvent.objects.filter(match_id = match_id,
                                  event_type__in = (MatchEventEnum.SCORE["type"][TeamSide.HOME], MatchEventEnum.SCORE["type"][TeamSide.AWAY])).count()
        if saved_goal_event_count < curr_goal_event_count:
            unsaved_goal_events = goal_events[saved_goal_event_count:]
            for event in unsaved_goal_events:
                scorer = event.get("home_scorer", "")
                event_type = MatchEventEnum.SCORE["type"][TeamSide.HOME]
                if scorer == "":
                    event_type = MatchEventEnum.SCORE["type"][TeamSide.HOME]
                    scorer = event.get("away_scorer", "")

                self.match_events.append({
                    "match_id" : match_id,
                    "event_type" : event_type,
                    "time" : event.get("time", 0),
                    "player_name" : re.sub(".*[.] ", '', scorer)})


    def save_to_db(self):
        logger.info("Saving matches to database")
        for match in self.match_infos:
            print(match)
            id = match["id"]
            match.pop("id")
            saved_match = Match.objects.update_or_create(id = id, defaults=match)

        for event in self.match_events:
            print(event)
            saved_event = MatchEvent.objects.create(**event)

        return True


def crawl_wc_2018_matches(live_only = False):
    WC_FROM_DATE = '2018-06-14'
    WC_TO_DATE = '2018-07-15'
    WC_league = Country.objects.get(en_name="World Cup 2018")
    WC_groups = League.objects.filter(country=WC_league)
    for group in WC_groups:
        crawler = MatchCrawler(group.id, WC_FROM_DATE, WC_TO_DATE, live = live_only)
        crawler.crawl()
        crawler.save_to_db()

if __name__ == "__main__":
    crawl_wc_2018_matches()