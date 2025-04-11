import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('./data/Global_Slavery_Index_2023.csv')
data.columns = data.columns.str.strip()  # Strip leading/trailing spaces from column names
print(data.describe())

# Convert Population and Estimated number of people in modern slavery to numeric (removing commas)
data["Population"] = data["Population"].str.replace(",", "","-").astype(float)
data["Estimated number of people in modern slavery"] = (
    data["Estimated number of people in modern slavery"].str.replace(",", "").astype(float)
)

# Check for missing values and display them
missing_values = data.isnull().sum()
print("Missing values in each column:\n", missing_values)


# Display cleaned dataset info and missing values
data.info(), missing_values



# Fill missing values using median for numerical columns
data["Population"].fillna(data["Population"].median(), inplace=True)
data["Estimated prevalence of modern slavery per 1,000 population"].fillna(
    data["Estimated prevalence of modern slavery per 1,000 population"].median(), inplace=True
)
data["Estimated number of people in modern slavery"].fillna(
    data["Estimated number of people in modern slavery"].median(), inplace=True
)

# Distribution of Modern Slavery Prevalence
plt.figure(figsize=(10, 5))
sns.histplot(data["Estimated prevalence of modern slavery per 1,000 population"], bins=20, kde=True, color="blue")
plt.title("Distribution of Estimated Prevalence of Modern Slavery per 1,000 Population")
plt.xlabel("Prevalence per 1,000 Population")
plt.ylabel("Count")
plt.show()

# Total number of people in modern slavery by region
total_by_region = data.groupby("Region")["Estimated number of people in modern slavery"].sum().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(
    x=total_by_region["Region"],
    y=total_by_region["Estimated number of people in modern slavery"],
    palette="Blues_d",
)
plt.title("Total Number of People in Modern Slavery by Region")
plt.xlabel("Region")
plt.ylabel("Total Number of People in Modern Slavery")
plt.xticks(rotation=45)
plt.show()

# Top 10 Countries with Highest Modern Slavery Prevalence
top_10_prevalence = data.nlargest(10, "Estimated prevalence of modern slavery per 1,000 population")
# top_10_prevalence.columns

plt.figure(figsize=(12, 6))
sns.barplot(
    y=top_10_prevalence["Country"],
    x=top_10_prevalence["Estimated prevalence of modern slavery per 1,000 population"],
    palette="Reds_r",
)
plt.title("Top 10 Countries with Highest Modern Slavery Prevalence (per 1,000 Population)")

plt.xlabel("Prevalence per 1,000 Population")
plt.ylabel(" Country")
plt.show()
