import pandas as pd

# Load all CSV files
df0 = pd.read_csv("data/daily_sales_data_0.csv")
df1 = pd.read_csv("data/daily_sales_data_1.csv")
df2 = pd.read_csv("data/daily_sales_data_2.csv")

# Combine datasets
df = pd.concat([df0, df1, df2], ignore_index=True)

# Keep only pink morsel rows
df = df[df["product"] == "pink morsel"]

# Remove dollar sign and convert price to float
df["price"] = df["price"].replace("[$]", "", regex=True).astype(float)

# Calculate sales
df["sales"] = df["price"] * df["quantity"]

# Keep only required columns
output = df[["sales", "date", "region"]]

# Save output
output.to_csv("formatted_sales_data.csv", index=False)

print("formatted_sales_data.csv created successfully")