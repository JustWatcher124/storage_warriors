import pandas as pd
import numpy as np


def main() -> None:
    return


def winsorize_column(df, column, quantile=0.05):
    """Winsorizes a specific column in a pandas dataframe at the given percentile."""
    if isinstance(quantile, tuple):
        lower_limit = np.percentile(df[column], 100 - quantile[0])  # upper percentile
        upper_limit = np.percentile(df[column], quantile[1])  # lower percentile

    # Calculate limits using numpy.percentile()
    else:
        lower_limit = np.percentile(df[column], 100 - quantile)  # upper percentile
        upper_limit = np.percentile(df[column], quantile)  # lower percentile

    # Winsorize the column using the limits calculated above
    df[column] = df[column].clip(lower=lower_limit, upper=upper_limit)

    return df[column]


def clean_dataframe(df: pd.DataFrame, winsorize_this_value: list = None, winsor_percentile: int = 5,
                    fillna_value: float = np.nan, date_column='date', drop_columns=[]) -> pd.DataFrame:
    """
        Available keyword arguments:
        - 'winsorize_columns' (list of strings): List of column names to be winsorized at the 5th percentile.
        - 'fillna_value' (scalar or function, optional): Value or function to fill NaN values. Default is np.nan.
        - 'dropna_rows' (boolean, optional): Whether to drop rows containing NaNs. Default is False.
    """

    # Fill na values with some value
    if callable(fillna_value) and fillna_value != float(0):
        df.fillna(fillna_value, inplace=True)
    else:
        df.dropna(inplace=False)

    if drop_columns:
        df.drop(drop_columns, axis=1, inplace=True)

    # Winsorize columns if specified
    if winsorize_this_value is not None:
        df[winsorize_this_value] = winsorize_column(df, winsorize_this_value, quantile=winsor_percentile)

    df[date_column] = pd.to_datetime(df[date_column])
    df['year'] = df[date_column].dt.year
    df['month'] = df[date_column].dt.month
    df['day'] = df[date_column].dt.day
    # df.to_csv('testing.csv')
    return df


if __name__ == '__main__':
    main()
