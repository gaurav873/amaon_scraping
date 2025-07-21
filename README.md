# Amazon Sponsored Product Scraper

This project scrapes sponsored product data from Amazon.in for a given keyword, analyzes the data, and presents it in a user-friendly Streamlit web app. It is designed to extract only sponsored products and provides clean, structured output for further analysis.

## Features
- Scrapes sponsored products from Amazon.in search results
- Extracts:
  - **Title**: Product name
  - **Brand**: Brand name
  - **Reviews**: Number of customer reviews
  - **Rating**: Average customer rating (out of 5)
  - **Selling Price**: Current price
  - **Image URL**: Product image link
  - **Product URL**: Link to the product page
- Saves data to CSV
- Streamlit UI for easy use

## Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/gaurav873/amaon_scraping.git
   cd amaon_scraping
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Run the Streamlit app:**
   ```bash
   streamlit run amazon_scraping/streamlit_app.py
   ```
2. **In your browser:**
   - Enter a keyword (e.g., "soft toys")
   - Click "Scrape Sponsored Products"
   - View and download the results as CSV

## Example Output Fields
| Title | Brand | Reviews | Rating | Selling Price | Image URL | Product URL |
|-------|-------|---------|--------|---------------|-----------|-------------|
| ...   | ...   | ...     | ...    | ...           | ...       | ...         |

## Notes
- Only sponsored products are scraped.
- The scraper uses Selenium to handle dynamic content.
- All dependencies are listed in `requirements.txt`.

## Repository
[https://github.com/gaurav873/amaon_scraping](https://github.com/gaurav873/amaon_scraping)
