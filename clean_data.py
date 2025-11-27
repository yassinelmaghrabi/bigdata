import pandas as pd
import numpy as np

file_path = "dirty_cafe_sales.csv"
df = pd.read_csv(file_path)


df.info()

print(df.describe(include="all"))


df_cleaned = df.copy()

for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce")
    if df_cleaned[col].isnull().any():
        median_val = df_cleaned[col].median()
        df_cleaned[col].fillna(median_val, inplace=True)
print(df_cleaned.isnull().sum())

for col in ["Price Per Unit", "Total Spent"]:
    non_numeric_original = df[pd.to_numeric(df[col], errors="coerce").isnull()][col]

for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    Q1 = df_cleaned[col].quantile(0.25)
    Q3 = df_cleaned[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df_cleaned[
        (df_cleaned[col] < lower_bound) | (df_cleaned[col] > upper_bound)
    ]


for col in ["Item", "Payment Method", "Location"]:
    if df_cleaned[col].isnull().any():
        df_cleaned[col].fillna("Unknown", inplace=True)
for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    if df_cleaned[col].isnull().any():
        df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)

initial_rows = df_cleaned.shape[0]
df_cleaned.drop_duplicates(inplace=True)


df_cleaned["Transaction Date"] = pd.to_datetime(
    df_cleaned["Transaction Date"], errors="coerce"
)
if df_cleaned["Transaction Date"].isnull().any():
    df_cleaned.dropna(subset=["Transaction Date"], inplace=True)

for col in ["Item", "Payment Method", "Location"]:
    df_cleaned[col] = df_cleaned[col].astype(str).str.strip().str.lower()

df_cleaned = df_cleaned[df_cleaned["Quantity"] > 0]
df_cleaned = df_cleaned[df_cleaned["Price Per Unit"] > 0]

df_cleaned["Total Spent"] = df_cleaned["Quantity"] * df_cleaned["Price Per Unit"]
print(df.head())

print(df_cleaned.head())

df.info()

df_cleaned.info()

output_file_path = "cafe_sales_cleaned.csv"
df_cleaned.to_csv(output_file_path, index=False)
