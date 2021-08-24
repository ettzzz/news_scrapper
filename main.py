# -*- coding: utf-8 -*-

from fastapi import FastAPI
from pydantic import BaseModel

from config.static_vars import API_PREFIX, DEBUG
from scheduler.schedule_maker import watcher, his_operator


class historicalWeightPost(BaseModel):
    start_date: str
    end_date: str


app = FastAPI(debug=DEBUG)


@app.get("/{}/live_weight".format(API_PREFIX))
def call_live_weight():
    results = watcher.get_code_weight()
    return results


@app.post("/{}/historical_weight".format(API_PREFIX))
def call_historical_weight(item: historicalWeightPost):
    start_date = item.start_date
    end_date = item.end_date
    fields, fetched = his_operator.get_feature_weights(start_date, end_date)
    # TODO: should we fix get_feature_weights from def?
    results = list()
    for f in fetched:
        results.append(dict(zip(fields, f)))
    return {'results': results}
