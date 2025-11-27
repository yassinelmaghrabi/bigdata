import pandas as pd
import numpy as np

file_path = "dirty_cafe_sales.csv"
df = pd.read_csv(file_path)


df.replace(["unknown", "UNKNOWN", "error", "ERROR"], np.nan, inplace=True)


print(df.head())


df_cleaned = df.copy()

for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce")


print(df_cleaned.isnull().sum())


for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    temp_series = df_cleaned[col].dropna()
    Q1 = temp_series.quantile(0.25)
    Q3 = temp_series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = temp_series[(temp_series < lower_bound) | (temp_series > upper_bound)]


for col in ["Item", "Payment Method", "Location"]:
    if df_cleaned[col].isnull().any():
        df_cleaned[col].fillna("unknown", inplace=True)
for col in ["Quantity", "Price Per Unit", "Total Spent"]:
    if df_cleaned[col].isnull().any():
        df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)


df_cleaned = df_cleaned[
    (df_cleaned["Quantity"].between(lower_bound, upper_bound))
    & (df_cleaned["Price Per Unit"].between(lower_bound, upper_bound))
]

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


df.info()

df_cleaned.info()

output_file_path = "cafe_sales_cleaned.csv"
df_cleaned.to_csv(output_file_path, index=False)
df_no_unknown = df_cleaned.copy()

cols_to_check = ["Item", "Payment Method", "Location"]
for col in cols_to_check:
    df_no_unknown = df_no_unknown[df_no_unknown[col] != "unknown"]

output_file_no_unknown = "cafe_sales_no_unknown.csv"
df_no_unknown.to_csv(output_file_no_unknown, index=False)
