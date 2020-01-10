import pandas as pd
def find_price_features(df):
    series_contains_prices = df.apply(contains_prices)
    price_cols = series_contains_prices[series_contains_prices].index
    return df[price_cols]

def find_percentage_features(df):
    series_contains_percentages = df.apply(contains_percentages)
    percentage_cols = series_contains_percentages[series_contains_percentages].index
    return df[percentage_cols]

def find_numeric_features(df):
    series_contains_number = df.apply(contains_numbers)
    return series_contains_number.index[series_contains_number.values]

def numeric_to_fix(df):
    numeric_features = find_numeric_features(df)
    return df[numeric_features].select_dtypes(exclude=['int64', 'float64'])[0:2]

def price_to_float(price):
    if type(price) == str and price[0] == '$':
        return float(price[1:].replace(',',''))


def contains_prices(column):
    regex_string = (r'^\$.*\d.*')
    return column.str.contains(regex_string).any()

def contains_percentages(column):
    regex_string = (r'^\d.*\%$')
    return column.str.contains(regex_string).any()

def contains_numbers(column):
    regex_string = (r'^(?!.*www|.*-|.*\/|.*[A-Za-z]|.* ).*\d.*')
#     regex_string = (r'\$\d+.*|\d+.*\%$|^\d+.*$')
    return column.str.contains(regex_string).any()

def prices_to_floats(df):
    price_features = df.columns
    prices_df = pd.DataFrame({})
    for feature in price_features:
        prices_df[feature] = df[feature].map(price_to_float)
    return prices_df.astype('float64')
    
def percentage_to_float(percentage):
    if type(percentage) == str:
        return float(percentage[:-1])

def percentages_to_floats(df):
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)
    percentage_features = df.columns
    percentages_df = pd.DataFrame({})
    for feature in percentage_features:
        percentages_df[feature] = df[feature].map(percentage_to_float)
    return percentages_df.astype('float64')
    
    
def merge_dfs(original_df, new_df):
    copied_original = original_df.copy()
    copied_original[new_df.columns] = new_df
    return copied_original