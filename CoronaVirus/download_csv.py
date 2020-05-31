import os
import pandas as pd
import gevent
from gevent import monkey

from CoronaVirus.utils import URL, ONE_DAY, START_DAY, TODAY, CSV_PATH

monkey.patch_all()

# CSV_PATH = os.path.join(os.path.dirname(__file__), 'static/daily_report/')
# URL = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/' \
#       r'csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'
# ONE_DAY = datetime.timedelta(days=1)
# START_DAY = datetime.date(2020, 1, 22)
# today = datetime.date(2020, 1, 31)
# TODAY = datetime.datetime.utcnow().date()
download_num = (TODAY - START_DAY).days
urls = [(URL.format((START_DAY + i * ONE_DAY).strftime('%m-%d-%Y')),
         (START_DAY + i * ONE_DAY).strftime('%m-%d-%Y') + '.csv') for i in range(download_num)]


def get_df(url, name):
    if os.path.exists(os.path.join(CSV_PATH, name)):
        return
    df = pd.read_csv(url)
    df.fillna(0, inplace=True)
    if 'Country/Region' in df.columns:
        df.rename(columns={'Country/Region': 'Country_Region'})
    df.to_csv(os.path.join(CSV_PATH, name))
    print('已下载{}'.format(name))


gevent.joinall([gevent.spawn(get_df, args[0], args[1]) for args in urls])
