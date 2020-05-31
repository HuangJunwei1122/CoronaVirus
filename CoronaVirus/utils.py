import datetime
import pandas as pd
import json
import os

TODAY = datetime.datetime.utcnow().date()
ONE_DAY = datetime.timedelta(days=1)
START_DAY = datetime.date(2020, 1, 22)
LAST_DAY = TODAY - ONE_DAY
URL = r'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/' \
      r'csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'
CSV_PATH = os.path.join(os.path.dirname(__file__), 'static/daily_report/')


def download_data(url, name):
    if os.path.exists(os.path.join(CSV_PATH, name)):
        return
    print('开始下载{}'.format(name))
    df = pd.read_csv(url)
    df.fillna(0, inplace=True)
    if 'Country/Region' in df.columns:
        df.rename(columns={'Country/Region': 'Country_Region'})
    df.to_csv(os.path.join(CSV_PATH, name))
    print('已下载{}'.format(name))


def fetch_daily():
    url = URL.format(LAST_DAY.strftime('%m-%d-%Y'))
    name = LAST_DAY.strftime('%m-%d-%Y') + '.csv'
    download_data(url, name)


def get_confirmed(date):
    # CSV_PATH = 'D:\\PC_projests\\test\\CoronaVirus\\CoronaVirus' \
    #            '\\static\\daily_report\\{}.csv'.format(date.strftime('%m-%d-%Y'))
    path = os.path.join(CSV_PATH, '{}.csv'.format(date.strftime('%m-%d-%Y')))
    try:
        df_daily = pd.read_csv(path)
    except FileNotFoundError:
        fetch_daily()
        df_daily = pd.read_csv(path)
    df_daily = df_daily[['Country_Region', 'Confirmed', 'Deaths', 'Recovered']]
    except_dup = df_daily['Country_Region'].drop_duplicates(keep=False)
    unique_counties = df_daily['Country_Region'].drop_duplicates(keep='first')
    dup_countries = except_dup.append(unique_counties, ignore_index=True).drop_duplicates(keep=False)
    for country in dup_countries:
        dup_data = df_daily.loc[df_daily['Country_Region'] == country]
        data_sum = dup_data.iloc[:, 1:].sum()
        df_sum = pd.DataFrame([[country] + [count for count in data_sum]], columns=dup_data.columns)
        df_daily = df_daily[df_daily['Country_Region'] != country].append(df_sum, ignore_index=True)
    if 'Active' not in df_daily.columns:
        df_daily['Active'] = df_daily['Confirmed'] - df_daily['Deaths'] - df_daily['Recovered']

    confirmed_sort = df_daily.sort_values(axis=0, ascending=False, by=['Confirmed'], ignore_index=True)
    active_sort = df_daily.sort_values(axis=0, ascending=False, by=['Active'], ignore_index=True)

    confirmed_sort = confirmed_sort[['Country_Region', 'Confirmed']].head(20)
    # json_confirmed = confirmed_sort.to_json(orient='split')
    # dict_confirmed = json.loads(json_confirmed)

    active_sort = active_sort[['Country_Region', 'Active']].head(20)
    # json_active = active_sort.to_json(orient='split')
    # dict_active = json.loads(json_active)
    data_set = pd.concat([confirmed_sort, active_sort], axis=1, ignore_index=True)
    json_data_set = data_set.to_json(orient='split')
    dict_data_set = json.loads(json_data_set)

    # return dict_confirmed['data'], dict_active['data']
    return dict_data_set['data']


def verify_date(date):
    if date < START_DAY or date > LAST_DAY:
        return False
    return True


