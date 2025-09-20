import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re

def perform_analysis_and_visualization(df_clean):
    """
    Part 3: Data Analysis and Visualization
    Performs analysis and creates visualizations.
    """
    print("\n--- Starting Data Analysis ---")

    # 1. Count papers by publication year
    papers_by_year = df_clean['year'].value_counts().sort_index()
    print(f"\n--- Papers by Year ---\n{papers_by_year}")

    # 2. Identify top journals
    # Fill NaN journals with 'Unknown' for analysis
    top_journals = df_clean['journal'].fillna('Unknown').value_counts().head(10)
    print(f"\n--- Top 10 Journals ---\n{top_journals}")

    # 3. Find most frequent words in titles (simple frequency)
    # Combine all titles, convert to lowercase, remove punctuation, split
    all_titles = ' '.join(df_clean['title'].fillna('').str.lower())
    # Simple cleaning: keep only letters and spaces
    all_titles_clean = re.sub(r'[^a-zA-Z\s]', ' ', all_titles)
    words = all_titles_clean.split()
    # Remove very common, non-informative words (basic stop words)
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'from', 'about', 'as', 'into', 'like', 'through', 'after', 'over', 'between', 'out', 'against', 'during', 'without', 'before', 'under', 'around', 'among'}
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    word_freq = pd.Series(filtered_words).value_counts().head(20)
    print(f"\n--- Top 20 Words in Titles ---\n{word_freq}")

    # Create visualizations
    plt.style.use('seaborn-v0_8') # Use a nice style

    # Plot 1: Publications over time
    plt.figure(figsize=(10, 6))
    plt.bar(papers_by_year.index, papers_by_year.values, color='skyblue', edgecolor='black')
    plt.title('Number of COVID-19 Research Publications by Year', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.xticks(papers_by_year.index)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('publications_by_year.png')
    plt.show()

    # Plot 2: Top Publishing Journals
    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis')
    plt.title('Top 10 Journals Publishing COVID-19 Research', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Publications')
    plt.ylabel('Journal')
    plt.tight_layout()
    plt.savefig('top_journals.png')
    plt.show()

    # Plot 3: Word Cloud of Paper Titles
    wordcloud_text = ' '.join(filtered_words)
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(wordcloud_text)

    plt.figure(figsize=(15, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of COVID-19 Paper Titles', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('title_wordcloud.png')
    plt.show()

    # Plot 4: Distribution of Paper Counts by Source (assuming 'source_x' is the source column)
    source_counts = df_clean['source_x'].value_counts()
    plt.figure(figsize=(10, 6))
    plt.pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Papers by Source', fontsize=14, fontweight='bold')
    plt.axis('equal') # Equal aspect ratio ensures pie is drawn as a circle.
    plt.tight_layout()
    plt.savefig('papers_by_source.png')
    plt.show()

    print("\nAll visualizations saved as PNG files.")

if __name__ == "__main__":
    # Load cleaned data
    df_clean = pd.read_csv('cleaned_metadata.csv')
    # Convert 'publish_time' back to datetime if needed (it might be read as string)
    df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'])
    perform_analysis_and_visualization(df_clean)