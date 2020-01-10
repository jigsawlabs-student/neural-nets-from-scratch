import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

def contains_date(column):
#     remove nas first, potentially use all
    regex_string = (r'^\d{1,2}-\d{1,2}-\d{4}$|^\d{4}-\d{1,2}-\d{1,2}$' + 
'|^\d{1,2}\/\d{1,2}\/\d{4}$|^\d{4}\/\d{1,2}\/\d{1,2}$')
    return column.str.contains(regex_string).any()

def find_date_features(df):
    series_contains_date = df.apply(contains_date)
    return series_contains_date.index[series_contains_date.values]

def to_dates(df):
    date_features = find_date_features(df)
    return df[date_features].astype('datetime64[ns]')

def generate_new_date_columns(dates_df):
    copied_dates_df = dates_df.copy()
    for col in copied_dates_df.columns:
        add_datepart(copied_dates_df, col)
    return copied_dates_df

def contains_time_ago(column):
    regex_string = (r'^\d.*ago$')
    return column.str.contains(regex_string).any()

def find_time_ago_features(df):
    series_contains_time_ago = df.apply(contains_time_ago)
    return series_contains_time_ago.index[series_contains_time_ago.values]

def merge_date_df(original_df, new_date_df):
    copied_original = original_df.copy()
    date_features = find_date_features(original_df)
    copied_dropped = copied_original.drop(columns = date_features)
    copied_dropped[new_date_df.columns] = new_date_df
    return copied_dropped

# for get_past_date, perhaps find most recent existing date in df

def get_past_date(str_days_ago, start_date = datetime.date.today()):
    splitted = str_days_ago.split()
    if splitted[0] == 'a':
        splitted[0] = 1
    if len(splitted) == 1 and splitted[0].lower() == 'today':
        return str(start_date.isoformat())
    elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
        date = start_date - relativedelta(days=1)
        return str(date.isoformat())
    elif len(splitted) == 1:
        np.nan
    elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
        date = start_date - relativedelta(hours=int(splitted[0]))
        return str(date.date().isoformat())
    elif splitted[1].lower() in ['day', 'days', 'd']:
        date = start_date - relativedelta(days=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
        date = start_date - relativedelta(weeks=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
        date = start_date - relativedelta(months=int(splitted[0]))
        return str(date.isoformat())
    elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
        date = start_date - relativedelta(years=int(splitted[0]))
        return str(date.isoformat())
    else:
        return "Wrong Argument format:" + splitted
    
import re
import pandas as pd
def add_datepart(df, fldname, drop=True, time=False, errors="raise"):
    fld = df[fldname]
    fld_dtype = fld.dtype
    if isinstance(fld_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        fld_dtype = np.datetime64

    if not np.issubdtype(fld_dtype, np.datetime64):
        df[fldname] = fld = pd.to_datetime(fld, infer_datetime_format=True, errors=errors)
    targ_pre = re.sub('[Dd]ate$', '', fldname)
    attr = ['Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
            'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start']
    if time: attr = attr + ['Hour', 'Minute', 'Second']
    for n in attr: df[targ_pre + n] = getattr(fld.dt, n.lower())
    df[targ_pre + 'Elapsed'] = fld.astype(np.int64) // 10 ** 9
    if drop: df.drop(fldname, axis=1, inplace=True)
        
        
# Ideas
# subtracting date columns from another 
# subtracting dates from additional key dates like holidays.  
# match dates to past temperatures if we believe this would help our dataset.