from typing import List
import pandas as pd
from itunes_app_scraper.scraper import AppStoreScraper
from itunes_app_scraper.util import AppStoreException


class TopHundredAppsRetriever:
    def __init__(self):
        self.scraper = AppStoreScraper()

    def get_top_100(self) -> List:
        """Fetch the top 100 iOS apps for the US from the app store and return their IDs"""
        results = self.scraper.get_apps_for_collection(country="US", num=100)
        print("Top 100 apps fetched")
        return [x['id']['attributes']['im:id'] for x in results['feed']['entry']]

    def get_app_details(self, app_id: str, sleep: int = 0):
        """Safely try to return details about an app"""
        try:
            return self.scraper.get_app_details(app_id, sleep=sleep)
        except AppStoreException:
            print(f"App {app_id} not found")
            return None

    def categorise_apps(self) -> pd.DataFrame:
        """
        Fetch the top 100 apps, categorise them as Kid friendly, as well as TV/Music/Game/Other, specifying other
        by primary genre. We use content rating to determine kid friendly, and some heuristics to determine the
        category, based on the genres returned by the app store search. This does return some false positives.
        """
        app_list = self.get_top_100()

        detailed_app_list = []
        for idx, app_id in enumerate(app_list):
            print(idx, app_id)
            app_details = self.get_app_details(app_id, sleep=5)
            if app_details is not None:
                detailed_app_list.append(app_details)
        print("App details fetched")

        df = pd.DataFrame(detailed_app_list)
        df["Kids friendly"] = df.trackContentRating != "17+"

        df["Category"] = "Other"

        # Note: there are no games in the top 100 apps that we fetched at the time of testing. Games are categorised
        # under the "Games" category, so we could use this paramter in the search. But we fetched the top 100 overall.
        df.loc[df.primaryGenreName.eq("Games"), "Category"] = "Game"
        df.loc[df.primaryGenreName.eq("Music"), "Category"] = "Music"

        # this gives some false positives - Jackpocket, Ticketmaster, Audible
        cond = (df.genres.str.contains("Entertainment")) & (df.Category.eq("Other"))
        df.loc[cond, "Category",] = "TV"

        df.loc[df.Category.eq("Other"), "Category"] = (
            "Other (" + df.loc[df.Category.eq("Other"), "primaryGenreName"] + ")"
        )
        return df
