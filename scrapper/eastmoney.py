# -*- coding: utf-8 -*-

import requests
import re
import random

from utils.datetime_tools import get_now, timestamper, DATE_TIME_FORMAT
from utils.gibber import logger


class eastmoneyScrapper():
    def __init__(self):
        self.base_url = 'https://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_1_.html'
        self.headers = {
            'Host': 'newsapi.eastmoney.com',
            'Referer': 'https://kuaixun.eastmoney.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
        }
        self.timestamp_format = DATE_TIME_FORMAT

    def _data_cleaner(self, news_dict):
        fid = news_dict['id']
        content = news_dict['digest'].strip()
        # timestamp = news_dict['showtime'] # already DATE_TIME_FORMAT
        timestamp = str(timestamper(news_dict['showtime'], self.timestamp_format))
        tag = news_dict['column']  # not sure what it stands for.

        code = re.findall(r'[(]([\d]{6})[)]', content)
        code = code[0] if len(code) > 0 else ''

        return {'fid': fid,
                'source': 'eastmoney',
                'content': content,
                'timestamp': timestamp,
                'tag': tag,
                'code': code,
                'industry': '',
                'info': '',
                'comment': ''
                }

    def get_params(self):
        params = {
            'r': str(random.random()),
            '_': str(int(get_now() * 1000))
        }
        return params

    def get_news(self, params, standard=True):
        r = requests.get(
            url=self.base_url,
            params=params,
            headers=self.headers,
            timeout=30)
        if r.status_code == 200:
            text = re.findall(r'ajaxResult=({.*})', r.text)[0]
            content = eval(text)
            if standard:
                cleaned_list = [self._data_cleaner(i) for i in content['LivesList']]
                # content['LivesList'] = cleaned_list
                content = cleaned_list
            return content
        else:
            logger.error('from eastmoneyScrapper: Requesting failed! check url \n{}'.format(r.url))
            return {}

if __name__ == "__main__":
    t = eastmoneyScrapper()
    p = t.get_params()
    n = t.get_news(p)