import pandas as pd
import os
"""
将下载的每日疫情csv文件进行数据预处理，得到累计确诊和当前确诊数据，并降序排列
"""


def output_one_csv():
    url_daily = os.path.join(os.path.dirname(__file__), 'static/daily_report/05-27-2020.csv')
    df_daily = pd.read_csv(url_daily)
    df_daily = df_daily.loc[:, ['Country_Region', 'Confirmed', 'Deaths', 'Recovered']]
    except_dup = df_daily['Country_Region'].drop_duplicates(keep=False)
    unique_counties = df_daily['Country_Region'].drop_duplicates(keep='first')
    dup_countries = except_dup.append(unique_counties, ignore_index=True).drop_duplicates(keep=False)
    for country in dup_countries:
        dup_data = df_daily.loc[df_daily['Country_Region'] == country]
        data_sum = dup_data.iloc[:, 1:].sum()
        df_sum = pd.DataFrame([[country]+[count for count in data_sum]], columns=dup_data.columns)
        df_daily = df_daily[df_daily['Country_Region'] != country].append(df_sum, ignore_index=True)

    if 'Active' not in df_daily.columns:
        df_daily['Active'] = df_daily['Confirmed'] - df_daily['Deaths'] - df_daily['Recovered']

    df_daily = df_daily.sort_values(axis=0, ascending=False, by=['Confirmed', 'Active'])
    print(df_daily)
