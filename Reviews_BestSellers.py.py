#!/usr/bin/env python
# coding: utf-8

# In[1]:


#What is the correlation between # of reviews and # of best sellers? Maybe look at the categories with  
#the highest numbers of these items?(Chris)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
import textwrap
from IPython.display import display

#File paths
amzCategoriesPath = r"C:\Users\cbush\OneDrive\Desktop\U of R Class\ProjectOneBootCamp\Amazon_US\amazon_categories.csv"
amzProductsPath = r"C:\Users\cbush\OneDrive\Desktop\U of R Class\ProjectOneBootCamp\Amazon_US\amazon_products.csv"

#Read csv's into dataframes
amzCategories = pd.read_csv(amzCategoriesPath)
amzProducts = pd.read_csv(amzProductsPath)

#Rename columns to prepare for merge
amzCategories = amzCategories.rename(columns= {"id" : "category_id"})

#Merge dataframes on 'category_id'
amzMerged = pd.merge(amzCategories, amzProducts, on="category_id", how="left")


# In[2]:


# Find rows where reviews are zero
zeroReviews = amzMerged[amzMerged["reviews"] == 0]

# Find rows among zero reviews where isBestSeller is True
zeroReviewsBestSellers = zeroReviews[zeroReviews["isBestSeller"] == True]

# Count total zero reviews and best sellers among them
print(f'There are {len(zeroReviews)} products with zero (0) reviews.')
print(f'{len(zeroReviewsBestSellers)} of these products are best sellers.')


# In[3]:


# Filter for products that are best sellers but have zero reviews
bestSellersNoReviews = amzMerged[(amzMerged['isBestSeller'] == True) & (amzMerged['reviews'] == 0)]

# Display the categories....(id's and names)
print("Categories of products that are best sellers but have no reviews:")
print(bestSellersNoReviews[['category_id', 'category_name', 'reviews', 'isBestSeller']])


# In[6]:


# Calculate category counts (Example: count of best sellers per category)
category_counts = amzMerged.groupby('category_name').agg(count=('isBestSeller', 'sum')).reset_index()

# Sort by the number of best sellers in descending order
sorted_category_counts = category_counts.sort_values(by='count', ascending=False)

# Select top 25 categories for the bar chart
top_categories = sorted_category_counts.head(25).copy()

# Wrap long category names for better readability
top_categories['wrapped_category_name'] = top_categories['category_name'].apply(
    lambda x: "\n".join(textwrap.wrap(x, width=20))
)

# Plot the horizontal bar chart
plt.figure(figsize=(12, 8))  # Increase figure size for readability
plt.barh(top_categories['wrapped_category_name'], top_categories['count'], color='skyblue')
plt.title('Top Categories of Best Sellers with No Reviews', fontsize=16)
plt.xlabel('Number of Best Sellers with No Reviews', fontsize=14)
plt.ylabel('Category', fontsize=14)
plt.gca().invert_yaxis()  # Invert y-axis to show highest values at the top

# Adjust y-tick spacing (increase padding)
plt.yticks(
    ticks=range(len(top_categories['wrapped_category_name'])),  # Ensure all labels align with bars
    labels=top_categories['wrapped_category_name'],
    fontsize=8,            # Adjust font size for clarity
    rotation=0,             # Keep labels horizontal
    verticalalignment='center'  # Ensure proper alignment
)

# Add space between ticks and plot
plt.tick_params(axis='y', which='major', pad=20)  # Increase padding for y-tick labels
plt.tight_layout()  # Ensure layout fits well
plt.savefig('TopCategoriesofBestSellersWithNoReviews.jpg', format='jpg', dpi=300)
plt.show()


# In[7]:


#drop rows that have zero reviews
amzMerged = amzMerged [amzMerged["reviews"] != 0]

#drop rows with NaN
amzMerged = amzMerged.dropna(subset=['reviews', 'isBestSeller'])


# In[8]:


# Convert 'Best Seller' (boolean) to numerical (1 for True, 0 for False)
amzMerged['isBestSeller'] = amzMerged['isBestSeller'].astype(int)


# Group by 'category_id' and 'category_name'
category_stats = amzMerged.groupby(['category_id', 'category_name']).agg({
    'reviews': 'sum',
    'isBestSeller': 'sum'
}).reset_index()


# In[9]:


# Correlation between # of Reviews and # of Best Sellers
correlation = category_stats[['reviews', 'isBestSeller']].corr()

print("Correlation between # of Reviews and # of Best Sellers:")
print(correlation)


# In[10]:


# Find top categories with the highest numbers
bestSellers = category_stats.sort_values(by=['isBestSeller', 'reviews'], ascending=False).head(10)

print("Top Categories with Highest # of Reviews and # of Best Sellers:")
print(bestSellers)


# In[11]:


# Sort categories by the number of best sellers in descending order
top_categories_stats = category_stats.sort_values(by='isBestSeller', ascending=False).head(25)

# Wrap long category names for better readability
top_categories_stats['wrapped_category_name'] = top_categories_stats['category_name'].apply(
    lambda x: "\n".join(textwrap.wrap(x, width=15))
)

# Scale reviews for better comparison (divide by 10,000)
scaling_factor = 100000
top_categories_stats['scaled_reviews'] = top_categories_stats['reviews'] / scaling_factor

# Set bar positions
categories = top_categories_stats['wrapped_category_name']
bar_width = 0.4
x_pos = np.arange(len(categories))

# Plot the side-by-side bar chart
plt.figure(figsize=(16, 10))
plt.bar(x_pos - bar_width/2, top_categories_stats['scaled_reviews'], bar_width, label=f'Reviews (scaled by {scaling_factor})', color='skyblue')
plt.bar(x_pos + bar_width/2, top_categories_stats['isBestSeller'], bar_width, label='Best Sellers', color='orange')

# Add category labels
plt.xticks(x_pos, categories, rotation=45, ha='right', fontsize=8)
plt.xlabel('Category', fontsize=10)
plt.ylabel('Count', fontsize=14)
plt.title('Top 25 Categories: Scaled Reviews vs Best Sellers', fontsize=16)
plt.legend()
plt.tight_layout()
plt.savefig('Top25CategoriesReviewsvBestSellers.jpg', format='jpg', dpi=300)
plt.show()


# In[12]:


# Find top categories with the highest numbers
top_categories = category_stats.sort_values(by=['reviews', 'isBestSeller'], ascending=False).head(10)

print("Top Categories with Highest # of Reviews and # of Best Sellers:")
print(top_categories[['category_id', 'category_name', 'reviews', 'isBestSeller']])


# In[13]:


# Sort categories by the number of reviews in descending order
top_categories_stats = category_stats.sort_values(by='reviews', ascending=False).head(25)

# Wrap long category names for better readability
top_categories_stats['wrapped_category_name'] = top_categories_stats['category_name'].apply(
    lambda x: "\n".join(textwrap.wrap(x, width=15))
)

# Scale reviews for better comparison (e.g., divide by 1,000)
scaling_factor = 100000
top_categories_stats['scaled_reviews'] = top_categories_stats['reviews'] / scaling_factor

# Set bar positions
categories = top_categories_stats['wrapped_category_name']
bar_width = 0.4
x_pos = np.arange(len(categories))  # Numeric positions for categories

# Plot the side-by-side bar chart
plt.figure(figsize=(16, 10))  # Adjust figure size for better spacing
plt.bar(x_pos - bar_width/2, top_categories_stats['isBestSeller'], bar_width, label='Best Sellers', color='orange')
plt.bar(x_pos + bar_width/2, top_categories_stats['scaled_reviews'], bar_width, label=f'Reviews (scaled by {scaling_factor})', color='skyblue')

# Add category labels
plt.xticks(x_pos, categories, rotation=45, ha='right', fontsize=8)
plt.xlabel('Category', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.title('Top 25 Categories: Best Sellers vs Scaled Reviews', fontsize=16)
plt.legend()
plt.tight_layout()  # Ensure everything fits well
plt.savefig('Top25CategoriesBestSellersvReviews.jpg', format='jpg', dpi=300)
plt.show()


# In[ ]:





# In[ ]:




