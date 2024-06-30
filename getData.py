import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import pandas as pd
import time
import re
from datetime import datetime, timedelta

# Loading environment variables from .env file
load_dotenv()
base_url = os.getenv('url')
print(base_url)

# Function to fetch data
def fetch_data(page_num):
    url = f"{base_url}{page_num}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    page = requests.get(url, headers=headers, timeout = 10)
    return BeautifulSoup(page.text, 'html')

# Finding desired elements
#find_date = soup.find_all('p', class_ = 'iLkEeQbexGs-')
#reviews = soup.find_all('span', class_ = 'l9bbXUdC9v0- ZatlKKd1hyc- ukvN6yaH1Ds-')
#soup.find_all('div', class_ = 'yEKDnyk-7-g-')

# Extracting usernames
def extract_usernames(soup):
    find_username = soup.find_all('p', class_ = '_1p30XHjz2rI- C7Tp-bANpE4-')
    usernames = [name.text.strip() for name in find_username]
    return usernames

# Extracting date
def extract_dates(soup):
    find_date = soup.find_all('p', class_ = 'iLkEeQbexGs-')
    dates = [date.text.strip() for date in find_date]
    return dates

# Extracting review content
def extract_reviews(soup):
    find_reviews = soup.find_all('span', class_ = 'l9bbXUdC9v0- ZatlKKd1hyc- ukvN6yaH1Ds-')
    review_text = [review.text.strip() for review in find_reviews if review.text.strip()]
    return review_text

# Looping through pages
max_pages = 50
page_num = 1

all_usernames = []
all_dates = []
all_reviews = []

while page_num <= max_pages:
    print(f"Fetching page {page_num}...")
    soup = fetch_data(page_num)

    usernames = extract_usernames(soup)
    dates = extract_dates(soup)
    reviews = extract_reviews(soup)

    all_usernames.extend(usernames)
    all_dates.extend(dates)
    all_reviews.extend(reviews)

    page_num += 1

    time.sleep(2)

# Creating a DataFrame
data = {
    'username': all_usernames,
    'date': all_dates,
    'review': all_reviews
}

df = pd.DataFrame(data)

print(df)

# Cleaning date column for import into SQL
def clean_date(date_str):
    pattern_absolute = r'Dined on (\w+ \d{1,2}, \d{4})'
    match_absolute = re.search(pattern_absolute, date_str)
    if match_absolute:
        return match_absolute.group(1)
    
    if 'days ago' in date_str:
        days_ago = int(re.search(r'(\d+) days ago', date_str).group(1))
        return (datetime.today() - timedelta(days = days_ago)).strftime('%B %d, %Y')
    
    return date_str

df['date'] = df['date'].apply(clean_date)

print(df)

df.dtypes

# converting to date 
df['date'] = pd.to_datetime(df['date'], errors='coerce')

print(df.dtypes)