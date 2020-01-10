import numpy as np
from explore import summarize_counts, remove_punctuation
import pandas as pd

def find_booleans(df):
    columns = df.columns
    boolean_columns = np.array([column for column in columns if len(df[column].value_counts(dropna=True)) == 2])
    boolean_values = np.array([df[column].value_counts(dropna=True).index.to_list() for column in boolean_columns])
    columns_and_values = np.stack((boolean_columns, boolean_values[:, 0], boolean_values[:, 1])).T
    return columns_and_values

def select_booleans(df, values = []):
    boolean_columns = find_booleans(df)
    matches = np.isin(boolean_columns[:, 1], values)
    return boolean_columns[matches]

def booleans_without_top_values(df, not_values = []):
    potential_new_features = matrix_new_features(df)
    not_tf = ~np.isin(potential_new_features[:, 1], not_values)
    return potential_new_features[not_tf]

def reduce_by(matrix, not_values = []):
    not_tf = ~np.isin(potential_new_features[:, 1], not_values)
    return potential_new_features[not_tf]

def to_booleans(df, boolean_mapping):
    boolean_values = list(boolean_mapping.keys())
    boolean_features = select_booleans(df, boolean_values)[:, 0]
    boolean_df = pd.DataFrame({})
    for feature in boolean_features:
        boolean_df[feature] = df[feature].map(boolean_mapping)
    return boolean_df[boolean_features]


def almost_binary(df, threshold = .95):
    return np.array([np.array([cat, top]) for cat, frequency, top in summarize_counts(df) if 1.0 > frequency > threshold])

def matrix_new_features(df):
    bin_feats = almost_binary(df)
    new_bin_feats = np.array(['{column}_is_{top}'.format(column = column, top = remove_punctuation(top)) for column, top in bin_feats])
    return np.hstack((bin_feats[:, 0].reshape(-1, 1), bin_feats[:, 1].reshape(-1, 1), new_bin_feats.reshape(-1, 1)))

def almost_to_boolean(df):
    matrix = matrix_new_features(df)
    columns_to_replace = matrix[:, 0]
    values_to_replace = matrix[:, 1]
    new_column_names = matrix[:, 2]
    to_replace_df = pd.DataFrame({})
    for column, value, new_name in zip(columns_to_replace, values_to_replace, new_column_names):
        bool_column = np.where(df[column] == value,1,0)
        to_replace_df[new_name] = bool_column
    return to_replace_df

def df_with_replaced_columns(original_df, selected_booleans_df, cols_to_drop = []):
    if len(cols_to_drop) == 0:
        cols_to_drop = selected_booleans_df.columns
    copied_df = original_df.copy()
    pruned_df = copied_df.drop(cols_to_drop, axis = 1)
    updated_bools_df = pd.concat([pruned_df, selected_booleans_df], axis = 1)
    return updated_bools_df