import pandas as pd
import helper_functions
import numpy as np


def main() -> None:
    return


def winsorize_column(df, column, quantile=0.05):
    """Winsorizes a specific column in a pandas dataframe at the given percentile."""

    # Calculate limits using numpy.percentile()
    lower_limit = np.percentile(df[column], (1 - quantile) * 100)  # upper percentile
    upper_limit = np.percentile(df[column], quantile * 100)  # lower percentile

    # Winsorize the column using the limits calculated above
    df[column] = df[column].clip(lower=lower_limit, upper=upper_limit)

    return df


def clean_dataframe(df: pd.DataFrame, winsorize_columns: list = None, winsor_percentile: float = 0.05, fillna_value: float = np.nan, dropna_rows: bool = False) -> pd.DataFrame:
    """
        Available keyword arguments:
        - 'winsorize_columns' (list of strings): List of column names to be winsorized at the 5th percentile.
        - 'fillna_value' (scalar or function, optional): Value or function to fill NaN values. Default is np.nan.
        - 'dropna_rows' (boolean, optional): Whether to drop rows containing NaNs. Default is False.
    """

    # Fill na values with some value
    if callable(fillna_value):
        df.fillna(fillna_value, inplace=True)
    else:
        df.fillna(fillna_value)

    # Winsorize columns if specified
    if winsorize_columns is not None:
        for column in winsorize_columns:
            df[column] = winsorize_column(df, column, quantile=winsor_percentile)

    # Drop rows containing NaNs if specified
    if dropna_rows:
        df.dropna(inplace=True)

    return df


if __name__ == '__main__':
    main()
