import numpy as np
from scipy import stats
import pandas as pd

def nas_sorted(df):
    '''Displays count of null values for each column'''     
    return df.isnull().sum().sort_values(ascending = False)

def impute_means(df):
    nan_cols = some_nans(df)
    col_means = df[nan_cols].mean()
    imputed_df = df.fillna(col_means)
    return imputed_df

### 2. Discover Outliers
def outlier_columns(df, threshold = .05):
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    outlier_columns = np.array([too_many_outliers(df[column]) for column in numeric_columns])
    return np.array([column for column in outlier_columns if column is not None])

def select_outliers(column, upper_tail = True):
    if upper_tail:
        return column[stats.zscore(column) > 2]
    else:
        return column[stats.zscore(column) < -2]

def percentiles(column):
    z_scores = stats.zscore(column)
    # segment based on number of standard deviations away from the mean     
    hist, bin_edges = np.histogram(z_scores, bins=np.arange(-3, 4, 1), density=True)
    return np.stack((hist, bin_edges[1:]))

def too_many_outliers(column, threshold = .05):
    '''expected .021 if normal distribution'''
    z_less_neg_two = percentiles(column)[0, 0]
    z_gt_two = percentiles(column)[0, -1]
    if z_less_neg_two > threshold or z_gt_two > threshold:
        return np.hstack((column.name, z_less_neg_two, z_gt_two))
    else:
        False
        

### 3. Add missing value columns
def new_df_with_na_cols(df):
    return pd.concat([df, new_na_columns(df)], axis = 1)

def informative(df):
    non_informative = [column for column in df.columns if len(df[column].unique()) == 1]
    informative_columns = list(set(df.columns.to_list()) - set(non_informative))
    return df[informative_columns]
    
def some_nans(df):
    informative_df = informative(df)
    some_nans_bools = pd.isnull(informative_df).any()
    return some_nans_bools.index[some_nans_bools]
    
def new_na_columns(df):
    nan_columns = some_nans(df)
    df_nans = pd.isnull(df[nan_columns])
    column_name_nas = ["{column_nan}_is_na".format(column_nan = column_nan) for column_nan in nan_columns]
    df_nans.columns = column_name_nas
    return df_nans

# 4. Additional Ideas
# Could treat values that repeat a lot as categorical
# For example, if lots of 99s or 99999 maybe that indicates something different. 

