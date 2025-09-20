import pandas as pd

def clean_and_prepare_data(df):
    """
    Part 2: Data Cleaning and Preparation
    Cleans the dataset and prepares it for analysis.
    """
    print("\n--- Starting Data Cleaning ---")

    # Create a copy to avoid modifying original
    df_clean = df.copy()

    # Handle missing data
    # For this assignment, we'll drop rows where critical info is missing
    initial_count = len(df_clean)
    df_clean = df_clean.dropna(subset=['title', 'publish_time'])
    final_count = len(df_clean)
    print(f"Dropped {initial_count - final_count} rows due to missing title or publish_time.")

    # Convert 'publish_time' to datetime
    # Handle potential errors by coercing invalid dates to NaT
    df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

    # Drop rows where date conversion failed
    before_drop = len(df_clean)
    df_clean = df_clean.dropna(subset=['publish_time'])
    after_drop = len(df_clean)
    print(f"Dropped {before_drop - after_drop} rows due to invalid publish_time.")

    # Extract year for time-based analysis
    df_clean['year'] = df_clean['publish_time'].dt.year

    # Create abstract word count (handle NaN abstracts)
    df_clean['abstract_word_count'] = df_clean['abstract'].fillna('').str.split().str.len()

    # Create title word count
    df_clean['title_word_count'] = df_clean['title'].str.split().str.len()

    print("\n--- Sample of Cleaned Data ---")
    print(df_clean[['title', 'publish_time', 'year', 'abstract_word_count', 'title_word_count']].head())

    # Save cleaned data for later use
    df_clean.to_csv('cleaned_metadata.csv', index=False)
    print("\nCleaned data saved to 'cleaned_metadata.csv'")

    return df_clean

# If running standalone, load the sample first
if __name__ == "__main__":
    from explore_data import load_and_explore_data
    df = load_and_explore_data()
    df_clean = clean_and_prepare_data(df)