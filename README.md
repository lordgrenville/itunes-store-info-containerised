# Home assignment for Peer39
This repo is originally forked from the DMI's [iTunes Store Scraper](https://github.com/digitalmethodsinitiative/itunes-app-scraper), which provides a simple Python wrapper around some HTTP requests to the iTunes store search. It has been changed extensively from that, though!

The first step of this assignment was to fetch the top 100 apps for 2022 from the Apple app store. This is easy to do with an HTTP `GET` request, which is wrapped in some well-tested Python classes.

The next step is to retrieve all data for these apps, and add the following classification:
* Kid friendly (for this I check if the `contentRating` is 17+)
* Category, out of `TV`, `Music`, `Game` or `Other`, with `Other` being specified. For this I used a couple of heuristics based on primary genre and other genres. Note that my method doesn't yield any games. This makes sense because there is a separate category for games on the app store (in fact there are multiple categories). It is possible to retrieve the top 100 games or the top 100 apps excluding most games, but not both together.

The next phase is to wrap this in a simple REST API, which I built using FastAPI. It exposes the following calls:

* `/summary`: get the top 100 apps
* `/details/{app_id}`: get details about a specific app (including categorisation)
* `/categorised_apps`: get all apps together with the categorisation (this can take a while, so it is suggested to use memoisation [I have added this option with `cache=True`])

Lastly, I created a Dockerfile describing a containerised version of this app, which could be run reproducibly on a server or as part of a Kubernetes cluster.

### Testing
Owing to the project structure and the nature of Python's import system, tests should be run from the project root directory with the command `python -m pytest`, rather than just `pytest`. Similarly, the server is started from root with the command `uvicorn src.api:app --host 0.0.0.0` (allowing us to port forward the app from the container to another server, eg I ran the container locally with the command `docker run --expose 8000 -p 8000:8000 peer39` [substituting whatever tag the Docker image has been built with]).

## Summary
This code runs an ASGI (asynchronous version of WSGI) server via [Uvicorn](https://www.uvicorn.org/). It exposes an endpoint (by default on port 8000) that receives HTTP requests and returns JSON output. The possible outputs are:
* the IDs for the top 100 apps from the iTunes Store
* full details for a specific app ID
* the top 100 apps categorised and whether they are kid-friendly

## Thoughts for scaling
If we wanted to increase load on this, it would be worth expanding the use of memoisation. For example, rather than call the iTunes API every time a request is received, responses could be stored along with a timestamp, and a new response fetched only after a certain interval. In the meantime, all requests could receive the cached response.
