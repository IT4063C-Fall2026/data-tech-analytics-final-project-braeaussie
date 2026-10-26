#!/usr/bin/env python
# coding: utf-8

# # The Impact of Rising Tuition on Student Loan Debt📝
# 
# ![Banner](./assets/banner.jpeg)

# ## Topic
# *What problem are you (or your stakeholder) trying to address?*
# 
# 📝 <!-- Answer Below -->
# Higher education costs in the United States have risen steadily for decades, outpacing wage growth and household income. As tuition increases, students rely more heavily on loans, leading to long-term financial strain, delayed homeownership, reduced savings, and widening socioeconomic gaps. This project aims to address the core problem: Is the growth in student loan debt primarily driven by rising tuition, stagnant income, or both? How has affordability changed over time?
# 

# ## Project Question
# *What specific question are you seeking to answer with this project?*
# <!--*This is not the same as the questions you ask to limit the scope of the project.*
# 📝 <!-- Answer Below -->
# How have rising tuition costs impacted student loan debt over the years, based on average student/household income?

# ## What would an answer look like?
# *What is your hypothesized answer to your question?*
# 📝 <!-- Answer Below -->
# 
# TUITION VS INCOME OVER TIME (LINE CHART)
# 
# Income ↑
# $90k |                               _____________
# $80k |                        ______/
# $70k |                 ______/
# $60k |          ______/
# $50k |   ______/
# $40k |__/
#        2000   2005   2010   2015   2020   2025
# 
# Tuition ↑
# $14k |                               __________________
# $12k |                        ______/
# $10k |                 ______/
#  $8k |          ______/
#  $6k |   ______/
#  $4k |__/
# 
# INTERPRETATION: Tuition rises faster than income, leading to a decline in affordability.

# ## Data Sources
# *What 3 data sources have you identified for this project?*
# *How are you going to relate these datasets?*
# 📝 <!-- Answer Below -->
# 
# .- College Tuition Dataset from College Board Trends in College Pricing (Table CP-3)
# 
# .- Median Household Income from U.S. Census ACS
# 
# .- Merged Final Dataset (merged on Year)

# ## Approach and Analysis
# *What is your approach to answering your project question?*
# *How will you use the identified data to answer your project question?*
# 📝 <!-- Start Discussing the project here; you can add as many code cells as you need -->

# In[2]:


#import
import os
import pandas as pd
from dotenv import load_dotenv
from fredapi import Fred
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import jupyter

load_dotenv(dotenv_path=r"C:\Users\braea\OneDrive\Documents\GitHub\data-tech-analytics-final-project-braeaussie\.env")
load_dotenv(override=True)


# In[ ]:


fred_api_key = os.getenv("FRED_API_KEY")
census_api_key = os.getenv("CENSUS_API_KEY")


# In[ ]:


# Load Data

# Tuition
tuition = pd.read_excel(
    "data/TrendsinCollegePricing2025.xlsx",
    sheet_name="Table CP-3",
    skiprows=2
)

# Student loan debt
fred = Fred(api_key=fred_api_key)

loan_debt = fred.get_series("SLOAS").to_frame(
    name="Student_Loan_Debt"
)

loan_debt.index = loan_debt.index.year

loan_debt = (
    loan_debt.groupby(loan_debt.index)
    .mean()
    .reset_index()
    .rename(columns={"index": "Year"})
)

# Income
income = fred.get_series("MEHOINUSA646N").to_frame(
    name="Median_Income")

income.index = income.index.year

income = (
    income.groupby(income.index)
    .mean()
    .reset_index()
    .rename(columns={"index": "Year"})
)


# In[ ]:


# Rename Tuition Academic Year --> Year
tuition = tuition.rename(columns={"Academic Year": "Year"})


# In[ ]:


# Convert Academic Years
tuition = tuition[
    tuition["Year"].astype(str).str.match(r"^\d{2}-\d{2}$", na=False)
]

tuition["Year"] = (
    tuition["Year"]
    .str[:2]
    .astype(int)
    .apply(lambda x: x + 1900 if x >= 86 else x + 2000)
)


# In[ ]:


df = tuition.merge(loan_debt, on="Year").merge(
    income[["Year", "Median_Income"]],
    on="Year",
    how="left"
)


# In[ ]:


# Save final dataset
df.to_csv("data/final_dataset.csv", index=False)

print(df.head())
print(df.info())


# In[ ]:


# Remove Unnamed/Unnecessary Columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]


# In[ ]:


# Rename Columns
df = df.rename(columns={
    "Public Two-Year": "Public Two-Year at the Time",
    "Public Four-Year": "Public Four-Year at the Time",
    "Private Nonprofit Four-Year": "Private Nonprofit Four-Year at the Time",
    "Public Two-Year.1": "Public Two-Year in 2025 Dollars",
    "Public Four-Year.1": "Public Four-Year in 2025 Dollars",
    "Private Nonprofit Four-Year.1": "Private Nonprofit Four-Year in 2025 Dollars"
})


# In[ ]:


# Add Average Tuition Columns
# Average tuition in current-year dollars
df["Average Tuition at the Time"] = (
    df[
        [
            "Public Two-Year at the Time",
            "Public Four-Year at the Time",
            "Private Nonprofit Four-Year at the Time"
        ]
    ]
    .mean(axis=1)
)

# Average tuition in 2025 dollars
df["Average Tuition in 2025 Dollars"] = (
    df[
        [
            "Public Two-Year in 2025 Dollars",
            "Public Four-Year in 2025 Dollars",
            "Private Nonprofit Four-Year in 2025 Dollars"
        ]
    ]
    .mean(axis=1)
)


# In[ ]:


# Initial Data Inspection

# How many records are available?
# What are the variable types?
# Are there missing values?
# What are the summary statistics?

df.info()

df.describe()

df.head()


# In[ ]:


# Tuition Over Time Line Chart
# Shows the historical growth of tuition at public four-year institutions in the United States.
plt.figure(figsize=(10,6))
plt.plot(df["Year"], df["Average Tuition in 2025 Dollars"], marker="o")
plt.title("Average College Tuition Over Time in 2025 Dollars")
plt.xlabel("Year")
plt.ylabel("Tuition ($)")
plt.grid(True)
plt.show()

# Tuition is expected to increase steadily over time, indicating rising educational costs.


# In[ ]:


# Student Loan Debt Over Time Line Chart
# Shows the historical growth of student loan debt in the United States.

plt.figure(figsize=(10,6))
plt.plot(
    df["Year"],
    df["Student_Loan_Debt"],
    color="red",
    marker="o"
)

plt.title("Student Loan Debt Over Time")
plt.xlabel("Year")
plt.ylabel("Debt (Millions of Dollars)")
plt.grid(True)
plt.show()

# Allows comparison between debt accumulation and tuition growth over time, highlighting the financial burden on students.


# In[ ]:


# Correlation Matrix Heatmap
# Shows the correlation between tuition, student loan debt, and median income in the United States.

plt.figure(figsize=(8,6))

sns.heatmap(
    df[[
        "Average Tuition in 2025 Dollars",
        "Student_Loan_Debt",
        "Median_Income"
    ]].corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Matrix")
plt.show()

# Allows comparisons between deb accumulation and tuition growth.

# Potential findings:
#   -Strong positive correlation between Tuition and Student Loan Debt.
#   -Weaker relationship between Income and Debt.
#   -Positive relationship between Income and Tuition.


# In[ ]:


# Distribution Analysis
# Examines how each variable is distributed.
fig, axes = plt.subplots(1,3, figsize=(15,5))

sns.histplot(df["Average Tuition in 2025 Dollars"], ax=axes[0])
axes[0].set_title("Average Tuition in 2025 Dollars")

sns.histplot(df["Student_Loan_Debt"], ax=axes[1])
axes[1].set_title("Student Loan Debt")

sns.histplot(df["Median_Income"], ax=axes[2])
axes[2].set_title("Median Income")

plt.tight_layout()
plt.show()

# Helps identify skewness and unusual observations in the data, which may affect analysis and modeling.


# What insights can be extracted?
# 
# . - Tuition has risen substantially over time.
# 
# . - Student loan debt appears to increase alongside tuition.
# 
# . - Household income has grown more slowly than tuition costs.
# 
# . - Affordability may have decreased over time.

# In[ ]:


# Are there correlations?
df.corr(numeric_only=True)

# 0.7 or greater = strong positive relationship
# 0.3-0.7 = moderate relationship
# below 0.3 = weak relationship


# In[ ]:


# Missing Values
df.isnull().sum()


# In[ ]:


# look for duplicate values
df.duplicated().sum()

# drop duplicates if they exist
# df = df.drop_duplicates()


# In[ ]:


# Verify data types
df.dtypes


# I already did a lot of cleaning before I merged the datasets, so my master dataset doesn't appear to need additional cleaning.

# In[ ]:


# look for outliers
# Because tuition and debt naturally rise over time, large values may represent genuine trends rather than errors.
sns.boxplot(data=df[[
    "Average Tuition in 2025 Dollars",
    "Student_Loan_Debt",
    "Median_Income"
]])


# In[ ]:


# Convert Data Types
df["Year"] = df["Year"].astype(int)

df["Average Tuition at the Time"] = pd.to_numeric(df["Average Tuition at the Time"])

df["Average Tuition in 2025 Dollars"] = pd.to_numeric(df["Average Tuition in 2025 Dollars"])

df["Student_Loan_Debt"] = pd.to_numeric(
    df["Student_Loan_Debt"]
)

df["Median_Income"] = pd.to_numeric(
    df["Median_Income"]
)


# Machine Learning Plan:
# 
# I plan to use a linear regression model to look at student loan debt. The predictors for this will be average tuition, median income, and the year. Linear regression is a continuous target variable that is easy to interpret, making it suitable for discovering relationships between education costs and debt.
# 
# My main challenge with this project is that I only have data from 1986-2025. Then, when I merged all of my datasets, it cut off anything before 2006. The problem with this is that smaller datsets limit model complexity. Another challenge is that the average tuition and year may be highly correlated, which would be multicollinearity because both variables are independent predictor variables. This can lead to inflated standard errors, unreliable p-values, unstable coefficients, or loss of interpretability. For example, if the average and tuition are correlated with each other, the model may struggle to determine if rising debt levels are caused by increasing tuition, the passage of time, or both. To address this issue, correlation analysis and Variance Inflation Factor (VIF) testing will be conducted. If severe multicollinearity is detected, highly correlated variables may be removed or Ridge Regression may be used to reduce its effects.

# ## Resources and References
# *What resources and references have you used for this project?*
# 📝 <!-- Answer Below -->

# In[3]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')


# In[6]:


import sys
get_ipython().system('{sys.executable} -m jupyter nbconvert --to python YourNotebook.ipynb')

