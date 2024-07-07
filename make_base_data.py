import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = 'orders factory.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Ensure the date column is in datetime format
data['date'] = pd.to_datetime(data['date'])

# Remove outliers where sales are above 250
data = data[data['sales'] <= 250]

# Add a year column
data['year'] = data['date'].dt.year

# Define the required years
required_years = set(range(2018, 2023))

# Group data by product and year, and count the occurrences
product_years = data.groupby(['product_id', 'year']).size().reset_index(name='count')

# Filter products that have sales in every required year
products_with_all_years = product_years[product_years['year'].isin(required_years)]
products_with_all_years = products_with_all_years.groupby(
    'product_id').filter(lambda x: set(x['year']) == required_years)

# Get the unique products that meet the criteria
valid_products = products_with_all_years['product_id'].unique()

# Filter the original sales data to include only valid products
filtered_data = data[data['product_id'].isin(valid_products)]

# Set the date as the index
filtered_data.set_index('date', inplace=True)

# Group by product_id and resample to weekly frequency, then compute the cumulative sum of sales per product
weekly_sales = filtered_data.groupby('product_id').resample('W').sum(
    numeric_only=True).groupby(level=0).cumsum().reset_index()

# Filter products based on cumulative sales thresholds
final_cumulative_sales = weekly_sales.groupby('product_id').last().reset_index()
filtered_product_ids = final_cumulative_sales[
    (final_cumulative_sales['sales'] >= 5000) &
    (final_cumulative_sales['sales'] <= 20000)
]['product_id']

# Filter the cumulative sales data to include only the valid products
filtered_cumulative_sales = weekly_sales[weekly_sales['product_id'].isin(filtered_product_ids)]

# Save the resulting data to a new CSV file
output_file_path = 'filtered_weekly_cumulative_sales.csv'
filtered_cumulative_sales.to_csv(output_file_path, index=False)

# Plotting function


def plot_sales_group(product_ids, sales_data):
    plt.figure(figsize=(15, 8))
    for product_id in product_ids:
        product_data = sales_data[sales_data['product_id'] == product_id]
        plt.plot(product_data['date'], product_data['sales'], label=f'Product {product_id}')
    plt.title('Cumulative Sales for Group of Products')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Quantity Sold')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Plot sales for products in groups of 20
unique_products = filtered_cumulative_sales['product_id'].unique()

wanted_data = data[data['product_id'].isin(unique_products)]

wanted_data.to_csv('wanted_data.csv', index=False)

# print(len(unique_products))
# group_size = 20
# for i in range(0, len(unique_products), group_size):
#    product_group = unique_products[i:i + group_size]
#    plot_sales_group(product_group, filtered_cumulative_sales)
