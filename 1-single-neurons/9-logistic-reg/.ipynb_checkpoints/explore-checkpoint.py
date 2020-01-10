import numpy as np
def summarize_counts(df):
    non_empty_columns = df.dropna(axis=1,how='all').columns
    frequencies = np.array([df[column].value_counts(normalize=True).values[0] for column in non_empty_columns]).reshape(-1, 1)
    columns = non_empty_columns.to_numpy().reshape(-1, 1)
    top_values = np.array([df[column].value_counts(normalize=True).index[0] for column in non_empty_columns]).reshape(-1, 1)
    summarize = np.hstack((columns, frequencies, top_values))
    return summarize[summarize[:,1].argsort()[::-1]]

def selected_summaries(df, not_values = [], lower_bound = .1, upper_bound = 1):
    potential_cols = summarize_counts(df)
    potential_cols = potential_cols[potential_cols[:, 1] > lower_bound]
    potential_cols = potential_cols[potential_cols[:, 1] < upper_bound]
    not_tf = ~np.isin(potential_cols[:, 2], not_values)
    return potential_cols[not_tf]

def reduce_by(matrix, not_values = []):
    not_tf = ~np.isin(matrix[:, 2], not_values)
    return matrix[not_tf]


def remove_punctuation(string):
    return string.strip().lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')

# 1. Discover Object Columns

def find_object_features(df):
    return list(df.dtypes[df.dtypes == 'object'].index)

def find_object_feature_values(df):
    object_features = find_object_features(df)
    return df[object_features][:2].values

# 1. Discover new missing data

def view_matches(df, match_value):
    '''Displays matches in dataframe; use in combo with df.replace'''
    matches = any_matches(df, match_value)
    if not matches.any():
        print('NO MATCHES FOR PROVIDED VALUE')
        return pd.DataFrame()
    match_columns = matches[:, 0]
    rows = np.concatenate(matches[:, 1])
    return df[match_columns].iloc[rows]

def column_matches(df, column, match_value):
    return np.array([column, df[df[column] == match_value].index.to_numpy()])

def any_matches(df, match_value):
    column_idx_matches = np.array([column_matches(df, column, match_value) for column in df.columns])
    return np.array(np.array([match for match in column_idx_matches if match[1].any()]))

