import pandas as pd

def load_and_explore_data():
    """
    Part 1: Data Loading and Basic Exploration
    Loads the sample dataset and performs initial exploration.
    """
    # Load the data (using sample for now)
    print("Loading dataset...")
    df = pd.read_csv('sample_metadata.csv')

    # Examine first few rows
    print("\n--- First 5 Rows ---")
    print(df.head())

    # Check DataFrame dimensions
    print(f"\n--- DataFrame Shape ---")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # Identify data types
    print(f"\n--- Data Types ---")
    print(df.dtypes)

    # Check for missing values in key columns
    key_columns = ['title', 'abstract', 'publish_time', 'journal', 'authors']
    print(f"\n--- Missing Values in Key Columns ---")
    print(df[key_columns].isnull().sum())

    # Generate basic statistics (for numerical if any, or just describe)
    print(f"\n--- Basic Statistics (describe) ---")
    print(df.describe(include='all'))

    return df

if __name__ == "__main__":
    df = load_and_explore_data()