import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import base64
from io import BytesIO

# Set page config
st.set_page_config(page_title="CORD-19 Data Explorer", layout="wide")

@st.cache_data
def load_data():
    """Load the cleaned dataset."""
    df = pd.read_csv('cleaned_metadata.csv')
    df['publish_time'] = pd.to_datetime(df['publish_time']) # Ensure datetime
    return df

def create_download_link(fig, filename):
    """Helper function to create a download link for a matplotlib figure."""
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">Download Plot</a>'
    return href

def main():
    st.title("CORD-19 Data Explorer")
    st.markdown("### A Simple Exploration of COVID-19 Research Papers")
    st.write("This application visualizes key trends from a sample of the CORD-19 research dataset.")

    # Load data
    df = load_data()

    # Sidebar for filters
    st.sidebar.header("Filters")
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    year_range = st.sidebar.slider(
        "Select Publication Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # Filter data based on selection
    df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Papers", len(df_filtered))
    with col2:
        st.metric("Unique Journals", df_filtered['journal'].nunique())
    with col3:
        avg_abstract_len = df_filtered['abstract_word_count'].mean()
        st.metric("Avg. Abstract Length", f"{avg_abstract_len:.1f} words")

    # Tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Publications Over Time", "📰 Top Journals", "☁️ Title Word Cloud", "🗃️ Data Sample"])

    with tab1:
        st.subheader("Publications Over Time")
        yearly_counts = df_filtered['year'].value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(yearly_counts.index, yearly_counts.values, color='lightcoral', edgecolor='black')
        ax.set_title('Number of Publications by Year', fontsize=14, fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Publications')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        st.pyplot(fig)
        st.markdown(create_download_link(fig, "publications_by_year.png"), unsafe_allow_html=True)

    with tab2:
        st.subheader("Top Publishing Journals")
        top_journals = df_filtered['journal'].fillna('Unknown').value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x=top_journals.values, y=top_journals.index, palette='magma', ax=ax)
        ax.set_title('Top 10 Journals', fontsize=14, fontweight='bold')
        ax.set_xlabel('Number of Publications')
        ax.set_ylabel('Journal')
        
        st.pyplot(fig)
        st.markdown(create_download_link(fig, "top_journals.png"), unsafe_allow_html=True)

    with tab3:
        st.subheader("Most Common Words in Titles")
        # Simple word frequency for the filtered data
        import re
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their', 'from', 'about', 'as', 'into', 'like', 'through', 'after', 'over', 'between', 'out', 'against', 'during', 'without', 'before', 'under', 'around', 'among'}
        
        all_titles = ' '.join(df_filtered['title'].fillna('').str.lower())
        all_titles_clean = re.sub(r'[^a-zA-Z\s]', ' ', all_titles)
        words = all_titles_clean.split()
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        if filtered_words:
            wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=50).generate(' '.join(filtered_words))
            fig, ax = plt.subplots(figsize=(15, 7))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title('Word Cloud of Paper Titles', fontsize=16, fontweight='bold')
            
            st.pyplot(fig)
            st.markdown(create_download_link(fig, "title_wordcloud.png"), unsafe_allow_html=True)
        else:
            st.write("No words to display for the selected filters.")

    with tab4:
        st.subheader("Sample of the Data")
        st.write(f"Showing {len(df_filtered)} papers from {year_range[0]} to {year_range[1]}.")
        # Display a sample of columns
        display_cols = ['title', 'authors', 'journal', 'publish_time', 'abstract_word_count']
        st.dataframe(df_filtered[display_cols].head(10), use_container_width=True)

    # Footer
    st.markdown("---")
    st.caption("Built with Streamlit for the Python Frameworks Assignment.")

if __name__ == "__main__":
    main()