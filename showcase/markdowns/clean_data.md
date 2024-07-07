# Clean the Data

Here you can select columns, values and other parameters for the cleaning process - after which, the dataset is made available to you. You can choose whether to train now or save the data and load it later.

[[[[

## 1. Select Columns to drop

As the program can not decide which columns are unnecessary, you can choose here yourself
[[[[

## 2. Where are the values?

Choose the column that contains the values that should be predicted, most times this column is something like \'item quantity\' or the like.
[[[[

## 3. Choose a value to replace missing values with

If you do not supply a value to replace the missing values in the dataset, we are forced to drop all rows containing non-existing values.
[[[[

## 4. Winsorization: Choose a percentile to fit outliers to

Winsorizing [(The Wikipedia page for Winsorizing)](https://en.wikipedia.org/wiki/Winsorizing) uses percentiles to limit extreme values / outliers in the dataset.
In short: With a 5th (the default) percentile winsorization the outliers that are above / below the percentile window between the 5th and 95th percentile get assigned the 5th or 95th percentile value respectively.
[[[[

## 5. Product column

Choose the column that denotes your product(s), be that ID, name or a number - this column is later used to ask the model for preditions.
[[[[

## 6. Date column

Tell the system what column contains the dates or timestamps. This column is very important.
[[[[

# Success!

You can now proceed to the next step: **Train or Save**. Just navigate to the page to directly train your data, or save your progress and train later.
