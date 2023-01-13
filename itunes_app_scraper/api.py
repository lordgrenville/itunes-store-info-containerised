from fastapi import FastAPI
from top_100_apps_details import TopHundredAppsRetriever

app = FastAPI()
t100 = TopHundredAppsRetriever()


@app.get("/")
def read_root():
    return "Healthy"


@app.get("/summary")
def top_hundred():
    return t100.get_top_100()


@app.get("/details/{app_id}")
def app_details(app_id: str):
    return t100.get_app_details(app_id, full_detail=True)


@app.get("/categorised_apps")
def get_categorised_apps():
    return t100.categorise_apps()
