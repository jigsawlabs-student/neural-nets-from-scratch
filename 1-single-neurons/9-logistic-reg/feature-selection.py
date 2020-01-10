def feature_importances(df, estimator):
    df_cols = df.columns[rfe.support_].to_numpy()
    coefs = estimator.coef_
    abs_coefs = abs(coefs)
    paired = np.hstack((df_cols.reshape(-1, 1), coefs.reshape(-1, 1), abs_coefs.reshape(-1, 1)))
    ordered_cols = paired[paired[:, -1].argsort()][::-1]
    return ordered_cols


from sklearn.feature_selection import RFE
def rfe_train_score(X_train, y_train, y_test, num_features):
    estimator = LinearRegression(n_jobs=-1)
    rfe = RFE(estimator, num_features, step=1)
    X_train_rfe = rfe.fit_transform(X_train,y_train)
    X_test_rfe = rfe.transform(X_test)
    estimator.fit(X_train_rfe,y_train)
    score = estimator.score(X_test_rfe,y_test)
    return np.array([estimator, score, idx])


def merge_multiple(df, match_strings):
    for string in match_strings:
        df = merge_cols(df, string)
    return df


def merge_cols(df, col_string):
    copied_df = df.copy()
    matched_cols = cols_contain(df, col_string)
    paired_df = df[matched_cols]
    merged_col = paired_df.max(axis = 1)
    copied_df[col_string] = merged_col
    return copied_df.drop(columns = matched_cols)

def cols_contain(df, string):
    return df.columns[df.columns.map(lambda col: string in col)].to_numpy()