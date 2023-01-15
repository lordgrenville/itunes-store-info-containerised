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

    def get_app_details(self, app_id: str, sleep: int = 0, full_detail=False):
        """
        Safely try to return details about an app. We have the option of returning raw data or categorising.
        When running on all 100 apps, it's more convenient to do it on the entire data set at once (as it's a
        vectorised operation). But the API allows us to query just one app along with categorisation.
        """
        try:
            details = self.scraper.get_app_details(app_id, sleep=sleep)
            if full_detail:
                details['Kid Friendly'] = details['contentAdvisoryRating'] != '17+'
                if details['primaryGenreName'] in ["Games", "Music"]:
                    details['Category'] = details['primaryGenreName']
                elif "Entertainment" in details['genres']:
                    details['Category'] = "TV"
                else:
                    details['Category'] = f"Other({details['primaryGenre']})"
            return details

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
