import pandas as pd

# Load the market cap data
marketcap_df = pd.read_csv("marketcap.csv", header=None, names=["Rank", "Symbol", "Company", "Market Cap"])
marketcap_df["Market Cap"] = marketcap_df["Market Cap"].str.replace("B", "").str.replace(",", "").astype(float) * 1e9
marketcap_df["Market Cap"] = marketcap_df["Market Cap"].astype(int)  # Convert to whole number

# Load the S&P 500 data
snp500_df = pd.read_csv("snp500.csv")

# Merge on the Symbol column
merged_df = snp500_df.merge(marketcap_df[["Symbol", "Market Cap"]], on="Symbol", how="left")

# Save the cleaned merged file
merged_df.to_csv("merged_snp500_marketcap.csv", index=False)
