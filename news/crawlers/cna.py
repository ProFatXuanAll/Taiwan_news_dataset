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


def get_news_list(
    current_datetime: datetime,
    past_datetime: datetime,
    *,
    debug: bool = False,
) -> List[News]:
    news_list: List[News] = []
    logger = Counter()

    date = current_datetime

    fail_count = 0
    date_str = date.strftime('%Y%m%d')

    # Only show progress bar in debug mode.
    iter_range = range(10000)
    if debug:
        iter_range = tqdm(iter_range)

    for i in iter_range:
        # No more news to crawl.
        if fail_count >= CONTINUE_FAIL_COUNT:
            break

        url = f'https://www.cna.com.tw/news/aipl/{date_str}{i:04d}.aspx'
        try:
            response = requests.get(
                url,
                timeout=news.crawlers.util.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.check_status_code(
                company='cna',
                response=response
            )

            # If `status_code == 200`, reset `fail_count`.
            fail_count = 0

            parsed_news = news.preprocess.cna.parse(ori_news=News(
                raw_xml=response.text,
                url=url,
            ))

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

    date = current_datetime
    # Commit database once a day.
    while date >= past_datetime:
        news.db.write.write_new_records(
            cur=cur,
            news_list=get_news_list(
                current_datetime=date,
                debug=debug,
                past_datetime=date - timedelta(days=1),
            ),
        )
        # Go back 1 day.
        date = date - timedelta(days=1)

        conn.commit()

    # Close database connection.
    conn.close()
