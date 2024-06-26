#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 20:42:04 2022

@author: ert
"""

import time
import random

import sys
sys.path.append("/home/ert/Desktop/git_repos/news_scrapper")
from database.news_operator import newsDatabaseOperator
from scrapper.yuncaijing import yuncaijingScrapper
from utils.datetime_tools import (
    get_now,
    get_today_date,
    get_delta_date,
    date_range_generator,
)
from utils.gibber import logger

def ycj_news_update(from_date=None):
    source = "ycj"
    _now = get_now(is_timestamp=False)
    today = get_today_date()

    if from_date is not None:
        dates = date_range_generator(from_date, today)
    else:
        if _now.hour == 0 and _now.minute <= 5:
            yesterday = get_delta_date(today, -1)
            dates = date_range_generator(yesterday, today)
        else:
            dates = date_range_generator(today, today)

    ys = yuncaijingScrapper()
    his_operator = newsDatabaseOperator()
    conn = his_operator.on()
    max_id = his_operator.get_latest_news_id(source=source, conn=conn)

    fetched = list()
    for date in dates:
        page = 1
        while page <= 40: ##
            ycj_params = ys.get_params(page, date)
            ycj_news = ys.get_news(ycj_params)  ## fid is descending
            logger.debug(f"{date},{len(ycj_news)}")
            time.sleep(15 + random.random())
            if len(ycj_news) == 0:
                break  ## page is too large, empty data
            if ycj_news[0]["fid"] <= max_id:
                break  ## the biggest fid is small/equal than max_id
            if ycj_news[-1]["fid"] <= max_id:
                for n in ycj_news:
                    if n["fid"] > max_id:
                        fetched.append(n)
                break
            else:
                for n in ycj_news:
                    if n["code"]:
                        fetched.append(n)
                page += 1

        if len(fetched) == 0:
            continue

        max_id = max(max_id, fetched[0]["fid"])
        his_operator.insert_news_data(fetched, source, conn)
        logger.info(f"from {__file__}: {date} finished with pages {page}, news {len(fetched)}.")
        fetched.clear()

    his_operator.off()
    return


if __name__ == "__main__":
    ycj_news_update("2024-04-12")