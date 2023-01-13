# Home assignment for Peer39
This repo is forked from the DMI's [iTunes Store Scaper](https://github.com/digitalmethodsinitiative/itunes-app-scraper), a simple Python scraper.

The first step of this assignment was to fetch the top 100 apps for 2022 from the Apple app store. This is easy to do with an HTTP `GET` request, which is wrapped in some well-tested Python classes.

The next step is to retrieve all data for these apps, and add the following classification:
* Kid friendly (for this I check if the `contentRating` is 17+)
* Category, out of TV, Music, Game or Other, with other being specified. For this I used a couple of heuristics based on primary genre and other genres. Note that my method doesn't yield any games. This makes sense because there is a separate category for games on the app store (in fact there are multiple categories). It is possible to retrieve the top 100 games or the top 100 apps excluding most games, but not both together.

The next phase is to wrap this in a simple REST API, which I built using FastAPI. It exposes the following calls:

* `/summary`: get the top 100 apps
* `/details/{app_id}`: get details about a specific app
* `/categorised_apps`: get all apps together with the categorisation.
