from collections import Counter
from datetime import datetime, timedelta
from typing import List

import dateutil.parser
import requests
from tqdm import tqdm

import news.crawlers
import news.db
from news.db.schema import News

CONTINUE_FAIL_COUNT = 100

CATEGORIES = {
    'A': '體育',
    'C': '一般',
    'F': '財經',
    'I': '國際',
    'J': '美食',
    'L': '生活',
    'N': '社會',
    'P': '政治',
    'R': '美食',
    'S': '社會',
    'U': '社會',
    'W': '一般',
}


def get_news_list(
    category: str,
    current_datetime: datetime,
    api: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
) -> List[News]:
    news_list: List[News] = []
    logger = Counter()

    date = current_datetime

    fail_count = 0
    date_str = \
        f'{date.strftime("%Y")}{int(date.strftime("%m")):x}{date.strftime("%d")}'

    if api == 'W':
        iter_range = range(10000)
    else:
        iter_range = range(30)

    # Only show progress bar in debug mode.
    if debug:
        iter_range = tqdm(iter_range)

    for i in iter_range:
        # No more news to crawl.
        if fail_count >= CONTINUE_FAIL_COUNT:
            break

        if api == 'W':
            url = f'https://www.ftvnews.com.tw/news/detail/{date_str}{api}{i:04}'
        else:
            url = f'https://www.ftvnews.com.tw/news/detail/{date_str}{api}{i:02}M1'

        try:
            response = requests.get(
                url,
                timeout=news.crawlers.util.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.check_status_code(
                company='ftv',
                response=response
            )

            parsed_news = news.preprocess.ftv.parse(ori_news=News(
                raw_xml=response.text,
                url=url,
            ))

            # If `status_code == 200` and successfully parsed (only happend when
            # such news is not missing), reset `fail_count`.
            fail_count = 0

            news_datetime = dateutil.parser.isoparse(parsed_news.datetime)

            news_list.append(parsed_news)
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])
            continue

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


def main(
    current_datetime: datetime,
    db_name: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
):
    if past_datetime > current_datetime:
        raise ValueError('Must have `past_datetime <= current_datetime`.')

    # Get database connection.
    conn = news.db.util.get_conn(db_name=db_name)
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)

    for api, category in CATEGORIES.items():
        date = current_datetime
        # Commit database once a day.
        while date >= past_datetime:
            news.db.write.write_new_records(
                cur=cur,
                news_list=get_news_list(
                    category=category,
                    current_datetime=date,
                    api=api,
                    debug=debug,
                    past_datetime=date - timedelta(days=1),
                ),
            )

            # Go back 1 day.
            date = date - timedelta(days=1)

            conn.commit()

    # Close database connection.
    conn.close()
