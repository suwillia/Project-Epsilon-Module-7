#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


# In[3]:


ama_cat_csv = Path("amazon_categories.csv")
ama_catDF= pd.read_csv(ama_cat_csv)
ama_prod_csv = Path("amazon_products.csv")
ama_prodDF= pd.read_csv("amazon_products.csv")


# In[12]:


# Select only the relevant columns from ama_prodDF
ama_prod_selected = ama_prodDF[['title', 'price', 'category_id','boughtInLastMonth' ]]

# Perform the join
combined_amaDF = ama_catDF.merge(ama_prod_selected, on='category_id')


# In[13]:


combined_amaDF.head()


# In[18]:


# Group by category_id
grouped_amaDF = combined_amaDF.groupby('category_id')

# Aggregate price by mean
agg_amaDF = grouped_amaDF.agg({'price': 'mean'})  

# Count the number of products per category
product_counts = grouped_amaDF['title'].count().reset_index(name='product_count')

# Group by category_id and include category_name in the summary
summary_ama = combined_amaDF.groupby('category_id').agg(
    category_name=('category_name', 'first'),  # Include category_name
    average_price=('price', 'mean'),          # Calculate average price
    total_price=('price', 'sum'),             # Calculate total price
    product_count=('title', 'count'),         # Count the number of products
    total_bought=('boughtInLastMonth', 'sum') # Total items bought in last month
).reset_index()

# Display the final summary
print(summary_ama)


# In[19]:


summary_ama.head(5)


# In[27]:


# Sort by average price and select top N categories
# Number of top categories to display
top_n = 20  # Adjust this to show more or fewer categories

# Sort by average price and select the top N categories
top_categories = summary.nlargest(top_n, 'average_price')

# Creating the bar chart
plt.figure(figsize=(12, 6))
plt.bar(top_categories['category_name'], top_categories['average_price'], color='skyblue')

# Adding labels and title
plt.xlabel('Category Name', fontsize=12)
plt.ylabel('Average Price', fontsize=12)
plt.title(f'Top {top_n} Categories by Average Price', fontsize=14)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Adjust layout to avoid overlap
plt.tight_layout()

# Show the plot
plt.show()




# In[28]:


# Calculate total sales per category (assuming 'total_price' is already calculated)
combined_amaDF['total_price'] = combined_amaDF['price'] * combined_amaDF['boughtInLastMonth']

# Group by category_id and calculate the total sales for each category
category_sales = combined_amaDF.groupby('category_id').agg(
    category_name=('category_name', 'first'),  # Get the category name
    total_sales=('total_price', 'sum')         # Sum total sales for each category
).reset_index()

# Step 2: Find the threshold for the top 10% of sales
sales_threshold = category_sales['total_sales'].quantile(0.9)

# Step 3: Filter out categories that fall within the top 10% of total sales
top_10_percent_categories = category_sales[category_sales['total_sales'] >= sales_threshold]

# Display the top 10% categories by total sales
print(top_10_percent_categories)


# In[29]:


# Plotting the top 10% categories
plt.figure(figsize=(12, 6))
plt.bar(top_10_percent_categories['category_name'], top_10_percent_categories['total_sales'], color='green')

# Adding labels and title
plt.xlabel('Category Name', fontsize=12)
plt.ylabel('Total Sales', fontsize=12)
plt.title('Top 10% Categories by Total Sales', fontsize=14)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Show the plot
plt.tight_layout()
plt.show()


# In[30]:


# Calculate total sales across all categories
total_sales_all_categories = category_sales['total_sales'].sum()

# Calculate the percentage of total sales for each category
category_sales['percentage_sales'] = (category_sales['total_sales'] / total_sales_all_categories) * 100

# Step 3: Find the categories that dominate the top 10% of total sales
sales_threshold = category_sales['total_sales'].quantile(0.9)
top_10_percent_categories = category_sales[category_sales['total_sales'] >= sales_threshold]

# Display the top 10% categories by percentage sales
print(top_10_percent_categories[['category_name', 'total_sales', 'percentage_sales']])


# In[31]:


# Plotting the top 10% categories by percentage sales
plt.figure(figsize=(12, 6))
plt.bar(top_10_percent_categories['category_name'], top_10_percent_categories['percentage_sales'], color='green')

# Adding labels and title
plt.xlabel('Category Name', fontsize=12)
plt.ylabel('Percentage of Total Sales', fontsize=12)
plt.title('Top 10% Categories by Percentage of Total Sales', fontsize=14)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Show the plot
plt.tight_layout()
plt.show()


# In[ ]:




