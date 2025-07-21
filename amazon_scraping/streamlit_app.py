import streamlit as st
import pandas as pd
from scrape_amazon_soft_toys import scrape_amazon_sponsored_products

st.title('Amazon.in Sponsored Product Scraper')

all_fields = ['Title', 'Brand', 'Reviews', 'Rating', 'Selling Price', 'Image URL', 'Product URL']

keyword = st.text_input('Enter product keyword:', 'soft toys')
max_pages = st.slider('Number of pages to scrape', 1, 10, 3)

if st.button('Scrape Sponsored Products'):
    with st.spinner('Scraping, please wait...'):
        try:
            df = scrape_amazon_sponsored_products(keyword, all_fields, max_pages)
            if df.empty:
                st.warning('No sponsored products found.')
            else:
                st.success(f'Found {len(df)} sponsored products!')
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button('Download CSV', csv, f'sponsored_{keyword.replace(" ", "_")}.csv', 'text/csv')
        except Exception as e:
            st.error(f'Error: {e}') 