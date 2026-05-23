"""
Laboratory Work No. 4 - Additional Task
Topic: Pandas Data Analysis (Series and DataFrame)
Version: 1.0
Developer: Maleeva Kira 453501
Date: 2026-05-06
"""

# Section a: Pandas Library

# 1. Import pandas
import pandas as pd
import numpy as np

# 2. & 3. Structure of Series and creating Series
# Creating Series from a list
series_from_list = pd.Series([10, 20, 30, 40, 50], name="Numbers")
print("\n1. Series from list:")
print(series_from_list)

# Creating Series from a dictionary
series_from_dict = pd.Series({"Math": 85, "Physics": 90, "Chemistry": 88}, name="Scores")
print("\n2. Series from dictionary:")
print(series_from_dict)

# 4. Function display (shows nicely formatted output in Jupyter, here just print)
print("\n3. Display Series (via print):")
print(series_from_list)

# 5. Accessing Series elements with .loc and .iloc
print("\n4. Accessing elements:")
print(f"   .iloc[0] (by position): {series_from_list.iloc[0]}")
print(f"   .loc[2] (by label): {series_from_list.loc[2]}")
print(f"   .loc['Physics'] (by index name): {series_from_dict.loc['Physics']}")

# 6. Creating DataFrame
# Creating sample dataset (football players) - similar to real Kaggle datasets
data = {
    "Player": ["Messi", "Ronaldo", "Mbappe", "Haaland", "Salah"],
    "Age": [36, 38, 25, 23, 31],
    "Goals": [32, 30, 41, 52, 24],
    "Assists": [20, 11, 17, 9, 13],
    "Wage": [450, 500, 350, 400, 280],
    "Aggression": [65, 80, 75, 85, 72]
}

df = pd.DataFrame(data)
print("\n5. DataFrame created from dictionary:")
print(df)


#  Section b: Basic Operations

# 2. Getting information about DataFrame (each parameter)
print("\n1. DataFrame information:")
print(f"   Shape: {df.shape}")
print(f"   Index: {df.index}")
print(f"   Columns: {df.columns.tolist()}")
print(f"   Data types:\n{df.dtypes}")
print(f"   Memory usage: {df.memory_usage(deep=True)}")
print(f"\n   Statistical summary (describe):")
print(df.describe())
print(f"\n   Missing values:\n{df.isnull().sum()}")

# 5. Indexing and data extraction: statistical methods
# Example: How many times higher is the average Goals of players with max Aggression
# compared to players with min Aggression?

print("\n2. Statistical comparison (Goals vs Aggression):")

# Find max and min values of Aggression
max_aggression = df["Aggression"].max()
min_aggression = df["Aggression"].min()

# Get groups of players
players_max_agg = df[df["Aggression"] == max_aggression]
players_min_agg = df[df["Aggression"] == min_aggression]

# Calculate mean Goals for each group
mean_goals_max_agg = players_max_agg["Goals"].mean()
mean_goals_min_agg = players_min_agg["Goals"].mean()

# Calculate ratio
ratio = mean_goals_max_agg / mean_goals_min_agg

print(f"\n   Players with max Aggression ({max_aggression}):")
print(f"      {players_max_agg[['Player', 'Goals', 'Aggression']].to_string(index=False)}")
print(f"      Average Goals: {mean_goals_max_agg:.2f}")

print(f"\n   Players with min Aggression ({min_aggression}):")
print(f"      {players_min_agg[['Player', 'Goals', 'Aggression']].to_string(index=False)}")
print(f"      Average Goals: {mean_goals_min_agg:.2f}")

print(f"\n   Result: Average Goals of players with max Aggression is {ratio:.2f} times higher")
print(f"   than average Goals of players with min Aggression. (rounded: {ratio:.2f})")


# Additional example using .loc/.iloc for indexing

# Set Player as index for better demonstration
df_indexed = df.set_index("Player")

print("\n1. DataFrame with Player as index:")
print(df_indexed)

print("\n2. .loc (label-based selection):")
print(f"   Single row (Messi):\n{df_indexed.loc['Messi']}")
print(f"\n   Multiple columns for Messi:\n{df_indexed.loc['Messi', ['Goals', 'Assists']]}")

print("\n3. .iloc (position-based selection):")
print(f"   First row: {df.iloc[0]}")
print(f"   First 3 rows, first 2 columns:\n{df.iloc[0:3, 0:2]}")