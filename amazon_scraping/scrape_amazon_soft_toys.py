import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

def extract_product_info(card, fields):
    # Only keep sponsored products
    sponsored = card.find(lambda tag: tag.name == 'span' and 'Sponsored' in tag.text)
    if not sponsored:
        return None
    data = {}

    # Brand: Only from <h2 class='a-size-mini s-line-clamp-1'><span>BRAND</span></h2>
    if 'Brand' in fields:
        brand = None
        mini_h2 = card.find('h2', class_='a-size-mini s-line-clamp-1')
        if mini_h2:
            brand_span = mini_h2.find('span')
            if brand_span and brand_span.text.strip():
                brand = brand_span.text.strip()
        data['Brand'] = brand if brand else 'N/A'

    # Title: Only from <a class='a-link-normal ...'> <h2> <span>
    if 'Title' in fields:
        title = None
        for a_tag in card.find_all('a', class_=lambda x: x and 'a-link-normal' in x):
            h2_tag = a_tag.find('h2')
            if h2_tag:
                span = h2_tag.find('span')
                if span and span.text.strip():
                    title = span.text.strip()
                    break
        data['Title'] = title if title else 'N/A'

    # Reviews: Only from <span id='acrCustomerReviewText'>
    if 'Reviews' in fields:
        reviews = None
        review_span = card.find('span', id='acrCustomerReviewText')
        if review_span:
            aria = review_span.get('aria-label', '')
            match = re.search(r'([\d,]+)', aria)
            if match:
                reviews = match.group(1).replace(',', '')
            else:
                text = review_span.get_text(strip=True)
                match = re.search(r'([\d,]+)', text)
                if match:
                    reviews = match.group(1).replace(',', '')
        data['Reviews'] = reviews if reviews else 'N/A'

    # Rating: Only from <span class='a-icon-alt'>
    if 'Rating' in fields:
        rating = None
        rating_tag = card.find('span', {'class': 'a-icon-alt'})
        if rating_tag and rating_tag.text.strip():
            rating = rating_tag.text.split(' ')[0]
        data['Rating'] = rating if rating else 'N/A'

    # Selling Price
    if 'Selling Price' in fields:
        price = None
        price_tag = card.find('span', {'class': 'a-price-whole'})
        if price_tag and price_tag.text.strip():
            price = price_tag.text.replace(',', '')
        data['Selling Price'] = price if price else 'N/A'

    # Image URL
    if 'Image URL' in fields:
        image_url = None
        img_tag = card.find('img', {'class': 's-image'})
        if img_tag and img_tag.get('src'):
            image_url = img_tag['src']
        data['Image URL'] = image_url if image_url else 'N/A'

    # Product URL
    if 'Product URL' in fields:
        product_url = None
        link_tag = card.find('a', {'class': 'a-link-normal', 'href': True})
        if link_tag and link_tag.get('href'):
            product_url = 'https://www.amazon.in' + link_tag['href']
        data['Product URL'] = product_url if product_url else 'N/A'

    return data if data else None

def scrape_amazon_sponsored_products(keyword, fields, max_pages=3):
    results = []
    search_query = keyword.replace(' ', '+')
    search_url = f'https://www.amazon.in/s?k={search_query}'

    # Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    for page in range(1, max_pages + 1):
        url = search_url + f'&page={page}'
        driver.get(url)
        time.sleep(3)  # Wait for JS to load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_cards = soup.find_all('div', {'data-component-type': 's-search-result'})
        for card in product_cards:
            info = extract_product_info(card, fields)
            if info:
                results.append(info)
        time.sleep(2)
    driver.quit()
    return pd.DataFrame(results)

if __name__ == '__main__':
    fields = ['Title', 'Brand', 'Reviews', 'Rating', 'Selling Price', 'Image URL', 'Product URL']
    df = scrape_amazon_sponsored_products('soft toys', fields, max_pages=3)
    df.to_csv('sponsored_soft_toys.csv', index=False)
    print(f'Scraped {len(df)} sponsored products. Data saved to sponsored_soft_toys.csv') 