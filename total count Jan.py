#!/usr/bin/env python
# coding: utf-8

# In[5]:


# Import pandas
import pandas as pd

# File paths
categories_file = "/Users/janlelie/Desktop/Git Hub Repositories/Project_1/amazon_categories.csv"
products_file = "/Users/janlelie/Desktop/Git Hub Repositories/Project_1/amazon_products.csv"

# Load the files
categories_df = pd.read_csv(categories_file)
products_df = pd.read_csv(products_file)

# Print column names for debugging
print("Categories Columns:", categories_df.columns)
print("Products Columns:", products_df.columns)


# In[6]:


# Import pandas library
import pandas as pd

# File paths
categories_file = "/Users/janlelie/Desktop/Git Hub Repositories/Project_1/amazon_categories.csv"
products_file = "/Users/janlelie/Desktop/Git Hub Repositories/Project_1/amazon_products.csv"

# Load the data
categories_df = pd.read_csv(categories_file)
products_df = pd.read_csv(products_file)

# Merge the data using the correct columns
merged_df = pd.merge(products_df, categories_df, left_on="category_id", right_on="id")

# Set the categories as the index
merged_df.set_index("category_name", inplace=True)

# Group by the category index and count the products in each category
category_counts = merged_df.groupby("category_name").size().reset_index(name='product_count')

# Set the category name as the index
category_counts.set_index("category_name", inplace=True)

# Add a new column after the index to indicate the count of products
category_counts['products_count_column'] = category_counts['product_count']

# Display the resulting DataFrame
print(category_counts)

# Optionally, save the resulting DataFrame
category_counts.to_csv("/Users/janlelie/Desktop/Git Hub Repositories/Project_1/category_product_counts.csv")


# In[7]:


# Identify the category with the most products
most_products_category = category_counts['product_count'].idxmax()
most_products_count = category_counts['product_count'].max()

# Display the result
print(f"The category with the most products is '{most_products_category}' with {most_products_count} products.")


# In[8]:


# Identify the category with the least products
least_products_category = category_counts['product_count'].idxmin()
least_products_count = category_counts['product_count'].min()

# Display the result
print(f"The category with the least products is '{least_products_category}' with {least_products_count} products.")


# In[12]:


import pandas as pd

# Ensure Pandas shows all rows in the DataFrame
pd.set_option('display.max_rows', None)

# Sort the DataFrame by product_count in descending order
sorted_category_counts = category_counts.sort_values(by='product_count', ascending=False)

# Print the sorted DataFrame
print(sorted_category_counts)


# In[26]:


# Drop duplicate columns
category_counts = category_counts.loc[:, ~category_counts.columns.duplicated()]

# Sort the DataFrame by product_count in descending order
sorted_category_counts = category_counts.sort_values(by='product_count', ascending=False)

# Display the cleaned and sorted DataFrame
pd.set_option('display.max_rows', None)  # Ensure all rows are shown
print(sorted_category_counts)


# In[27]:


sorted_category_counts


# In[30]:


# Add a numbering column starting from 1
sorted_category_counts['row_number'] = range(1, len(sorted_category_counts) + 1)

# Display the updated DataFrame
pd.set_option('display.max_rows', None)  # Ensure all rows are shown
sorted_category_counts


# In[31]:


# Assuming `merged_df` is the original DataFrame created after merging products_df and categories_df

# Filter rows where isBestSeller is True
bestseller_df = merged_df[merged_df['isBestSeller'] == True]

# Group by category_id and count the number of True values
bestseller_counts = bestseller_df.groupby('category_id').size().reset_index(name='bestseller_count')

# Find the category_id with the most True values
most_bestseller_category_id = bestseller_counts.loc[bestseller_counts['bestseller_count'].idxmax(), 'category_id']
most_bestseller_count = bestseller_counts['bestseller_count'].max()

# Display the result
print(f"The category_id with the most 'True' values in 'isBestSeller' is {most_bestseller_category_id} with {most_bestseller_count} bestsellers.")

# Optionally, display the counts DataFrame
print(bestseller_counts)


# In[32]:


# Group by category_id and calculate the average stars for each unique category_id
average_stars_by_category = (
    merged_df.groupby('category_id')['stars']
    .mean()
    .reset_index(name='average_stars')
)

# Display the result
print(average_stars_by_category)

# Optionally, save the result to a CSV file
average_stars_by_category.to_csv("/Users/janlelie/Desktop/Git Hub Repositories/Project_1/average_stars_by_category.csv", index=False)


# In[39]:


# Filter out rows with NaN in the average_stars column
valid_average_stars = average_stars_by_category.dropna(subset=['average_stars'])

# Find the category with the highest average stars
highest_avg_category = valid_average_stars.loc[valid_average_stars['average_stars'].idxmax()]
highest_avg_df = pd.DataFrame([highest_avg_category]).rename(columns={"category_id": "Category with Highest Average Stars"})

# Find the category with the least average stars
lowest_avg_category = valid_average_stars.loc[valid_average_stars['average_stars'].idxmin()]
lowest_avg_df = pd.DataFrame([lowest_avg_category]).rename(columns={"category_id": "Category with Lowest Average Stars"})

# Combine the results into a single DataFrame
highest_and_lowest_avg_df = pd.concat([highest_avg_df, lowest_avg_df], axis=1)

# Display the resulting DataFrame
highest_and_lowest_avg_df


# In[40]:


# Filter out rows with NaN in the reviews column
valid_reviews = merged_df.dropna(subset=['reviews'])

# Group by category_id and calculate the total reviews for each unique category_id
total_reviews_by_category = (
    valid_reviews.groupby('category_id')['reviews']
    .sum()
    .reset_index(name='total_reviews')
)

# Find the category with the highest number of reviews
highest_reviews_category = total_reviews_by_category.loc[total_reviews_by_category['total_reviews'].idxmax()]
highest_reviews_df = pd.DataFrame([highest_reviews_category]).rename(columns={"category_id": "Category with Highest Reviews"})

# Find the category with the least number of reviews
lowest_reviews_category = total_reviews_by_category.loc[total_reviews_by_category['total_reviews'].idxmin()]
lowest_reviews_df = pd.DataFrame([lowest_reviews_category]).rename(columns={"category_id": "Category with Lowest Reviews"})

# Combine the results into a single DataFrame
highest_and_lowest_reviews_df = pd.concat([highest_reviews_df, lowest_reviews_df], axis=1)

# Display the resulting DataFrame
highest_and_lowest_reviews_df


# In[41]:


print(total_reviews_by_category)


# In[42]:


import matplotlib.pyplot as plt

# Filter rows where reviews and stars are valid (not NaN)
valid_data = merged_df.dropna(subset=['reviews', 'stars'])

# Calculate the correlation between reviews and stars
correlation = valid_data['reviews'].corr(valid_data['stars'])

# Display the correlation result
print(f"The correlation between reviews and star ratings is: {correlation:.2f}")

# Create a scatter plot to visualize the relationship
plt.figure(figsize=(10, 6))
plt.scatter(valid_data['reviews'], valid_data['stars'], alpha=0.5)
plt.title(f"Scatter Plot of Reviews vs Star Ratings (Correlation: {correlation:.2f})")
plt.xlabel("Number of Reviews")
plt.ylabel("Star Ratings")
plt.grid(True)
plt.show()


# In[ ]:




