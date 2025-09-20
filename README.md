# Simple README for CORD-19 Data Explorer

This is a simple project that analyzes COVID-19 research papers and shows the results in a web app.

## How It Works

The project has 4 main Python files that you run in order:

1.  **`explore_data.py`**
    *   **What it does:** Loads the data and shows you basic information about it (like how many rows/columns, what data is missing).
    *   **Run it first:** `python explore_data.py`

2.  **`clean_data.py`**
    *   **What it does:** Cleans up the data. It removes bad rows, fixes the dates, and adds helpful new columns (like counting words in the title).
    *   **Run it second:** `python clean_data.py`
    *   *It saves the cleaned data to a new file called `cleaned_metadata.csv`.*

3.  **`analyze_and_visualize.py`**
    *   **What it does:** Analyzes the cleaned data and creates charts (like publications per year, top journals, and a word cloud).
    *   **Run it third:** `python analyze_and_visualize.py`
    *   *It saves the charts as PNG image files.*

4.  **`app.py`**
    *   **What it does:** This is the web application! It uses Streamlit to create an interactive website where you can see the charts and filter the data by year.
    *   **Run it last:** `streamlit run app.py`
    *   *This will open a browser window with the app.*

## To Get Started

1.  Put all the files (including `sample_metadata.csv`) in one folder.
2.  Open a terminal/command prompt in that folder.
3.  Install the needed tools:
    `pip install pandas matplotlib seaborn streamlit wordcloud`
4.  Run the 4 Python files in order (steps 1-4 above).

