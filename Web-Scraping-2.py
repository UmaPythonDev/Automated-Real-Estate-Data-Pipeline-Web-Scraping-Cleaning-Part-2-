import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\data\magicbricks_chennai.csv")


def inspect_data(df):
    print("\nData Overview:")
    print(df.info())
    print("\nFirst Few Rows:")
    print(df.head())

def clean_data(df):
    print("\nHandling Missing Data...")
    
    # Replace invalid values with NaN
    df.replace({'—': np.nan, 'N/A': np.nan, '': np.nan}, inplace=True)
    
    # Drop rows with missing essential values
    df.dropna(subset=["Price", "Title", "Link", "Image URL"], inplace=True)
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    print(f"Cleaned Data: {len(df)} rows remaining.")
    return df


def clean_price(value):
    """Convert price string like '96 Lac', '1.2 Cr', '₹56,000' into float (in INR)."""
    if isinstance(value, str):
        value = value.replace("\n", "").replace("₹", "").replace(",", "").strip().lower()
        if "lac" in value:
            return float(re.findall(r"[\d\.]+", value)[0]) * 1e5
        elif "cr" in value or "crore" in value:
            return float(re.findall(r"[\d\.]+", value)[0]) * 1e7
        elif re.search(r"[\d\.]+", value):
            return float(re.findall(r"[\d\.]+", value)[0])
        else:
            return np.nan
    return np.nan


def convert_columns(df):
    print("Converting Columns...")
    
    # Strip whitespace from all cells
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Convert Price column using clean_price()
    df['Price'] = df['Price'].apply(clean_price)
    
    # Convert Title column
    df['Title'] = df['Title'].astype(str).str.strip()
    df['Title'].fillna("No Title", inplace=True)
    
    # Convert Link column
    df['Link'] = df['Link'].astype(str).str.strip()
    df['Link'].fillna("No Link", inplace=True)
    
    # Convert Image URL
    df['Image URL'] = df['Image URL'].astype(str).str.strip()
    
    print("Data Cleaning Complete!")
    return df

def summarize_data(df):
    print("\nSummary Statistics:")
    print(df.describe())


def plot_price_distribution(df):
    plt.figure(figsize=(10,5))
    sns.histplot(df['Price'].dropna(), bins=30, kde=True)
    plt.xlabel("Price (INR)")
    plt.ylabel("Count")
    plt.title("Price Distribution of Listings")
    plt.show()


def show_extreme_listings(df):
    print("\nTop 5 Most Expensive Listings:")
    print(df.nlargest(5, 'Price')[['Title', 'Price', 'Link']])
    
    print("\nTop 5 Cheapest Listings:")
    print(df.nsmallest(5, 'Price')[['Title', 'Price', 'Link']])

if __name__ == "__main__":
    inspect_data(df)
    df = clean_data(df)
    df = convert_columns(df)
    summarize_data(df)
    plot_price_distribution(df)
    show_extreme_listings(df)
    
    # Save the cleaned dataset
    df.to_csv(r"C:\data\magicbricks_chennai_cleaned.csv", index=False)
    print("Cleaned data saved as 'magicbricks_chennai_cleaned.csv'.")
    print("Data Pipeline Completed Successfully!")
    """Clean the DataFrame by handling missing values and invalid entries."""
