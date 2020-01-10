import numpy as np
import pandas as pd
from explore import summarize_counts, remove_punctuation
from scipy import stats

def percentage_unique(df_series):
    series_filled = df_series.dropna()
    return len(series_filled.unique())/len(series_filled)

def find_categorical(df, threshold = .5):    
    categorical_df = pd.DataFrame({})
    for column in df.columns:
        if percentage_unique(df[column]) < threshold:
            categorical_df[column] = df[column]
    return categorical_df 

def num_is_digit(array, str_index = 0):
    return np.array([value[str_index].isdigit() for value in array])

def remove_digits_from_selected(selected_matrix, col_idx, str_indices = [0, -1]):
    for idx in str_indices:
        selected_col = selected_matrix[~num_is_digit(selected_matrix[:, col_idx], idx)]
    return selected_col

def categorical_plus_values(df, threshold = 5):
    categorical_cols = find_categorical(df)
    return [column for column in categorical_cols if len(df[column].value_counts()) > threshold]

def selected_cat_values(column, threshold = .02):
    values_counted = column.value_counts(normalize=True)
    return values_counted[values_counted > threshold]

def reduce_cat_values(column, threshold = .02):
    column = column.copy()
    selected_values = selected_cat_values(column, threshold).index
    column[~column.isin(selected_values)] = 'other'
    return column.astype('category')

def df_reduced_categories(df, categoricals = [], threshold = .01):
    if len(categoricals) == 0:
        categoricals = df.columns
    new_df = pd.DataFrame()
    for category in categoricals:
        new_df[category] = reduce_cat_values(df[category], threshold)
    return new_df

def replace_df_columns(original_df, replacing_df):
    replacing_cols = replacing_df.columns
    original_df = original_df.drop(columns = replacing_cols)
    new_df = pd.concat([original_df, replacing_df], axis = 1)
    return new_df