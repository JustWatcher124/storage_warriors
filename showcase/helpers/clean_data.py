# Import needed modules for the functions in this file
import pandas as pd
import numpy as np

# this file should not be executed directed, imported (from)


def main() -> None:
    return


def winsorize_column(df, column, quantile=0.05):
    """Winsorizes a specific column in a pandas dataframe at the given percentile."""
    # handle differing upper and lower bounds input
    if isinstance(quantile, tuple):
        # Calculate limits using numpy.percentile()
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

    # Fill na values with some value or drop the value if the value was set to 0
    if callable(fillna_value) and fillna_value != float(0):
        df.fillna(fillna_value, inplace=True)
    else:
        df.dropna(inplace=False)

    # drop columns from dataframe
    if drop_columns:
        df.drop(drop_columns, axis=1, inplace=True)

    # Winsorize columns if specified
    if winsorize_this_value is not None:
        df[winsorize_this_value] = winsorize_column(df, winsorize_this_value, quantile=winsor_percentile)

    # feature engineering from date column
    df[date_column] = pd.to_datetime(df[date_column])
    df['year'] = df[date_column].dt.year
    df['month'] = df[date_column].dt.month
    df['day'] = df[date_column].dt.day
    return df


# this file should not be executed directly, only imported (from)
if __name__ == '__main__':
    main()
