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
# find_date = soup.find_all('p', class_ = 'iLkEeQbexGs-')
# reviews = soup.find_all('span', class_ = 'l9bbXUdC9v0- ZatlKKd1hyc- ukvN6yaH1Ds-')
# [rating_header.text.strip() for rating_header in soup.find_all('li', class_ = '-k5xpTfSXac-')]
# [rating.text.strip() for rating in soup.find_all('span', class_ = '-y00OllFiMo-')]

# Extracting usernames
def extract_usernames(soup):
    find_username = soup.find_all('p', class_ = '_1p30XHjz2rI- C7Tp-bANpE4-')
    usernames = [name.text.strip() for name in find_username]
    return usernames

# Extracting ratings
def extract_ratings(soup):
    find_rating = soup.find_all('li', class_ = '-k5xpTfSXac-')
    ratings = [rating.text.strip().rsplit() for rating in find_rating]
    # rating_headers = pd.Series([rating[:-2] for rating in rating]).drop_duplicates().tolist()
    return ratings

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
all_ratings = []
all_dates = []
all_reviews = []

while page_num <= max_pages:
    print(f"Fetching page {page_num}...")
    soup = fetch_data(page_num)

    usernames = extract_usernames(soup)
    ratings = extract_ratings(soup)
    dates = extract_dates(soup)
    reviews = extract_reviews(soup)

    all_usernames.extend(usernames)
    all_ratings.extend(ratings)
    all_dates.extend(dates)
    all_reviews.extend(reviews)

    page_num += 1

    time.sleep(2)

# Creating a DataFrame for username, date, review
review_data = {
    'username': all_usernames,
    'date': all_dates,
    'review': all_reviews
}
df_reviews = pd.DataFrame(review_data)
print(df_reviews)

# Cleaning date column for import into SQL
def clean_date(date_str):
    pattern_absolute = r'Dined on (\w+ \d{1,2}, \d{4})'
    match_absolute = re.search(pattern_absolute, date_str)
    if match_absolute:
        return match_absolute.group(1)
    
    if 'day ago' in date_str:
        return (datetime.today() - timedelta(days = 1)).strftime('%B %d, %Y')
    
    if 'days ago' or 'day ago' in date_str:
        days_ago = int(re.search(r'(\d+) days ago', date_str).group(1))
        return (datetime.today() - timedelta(days = days_ago)).strftime('%B %d, %Y')
    
    return date_str

df_reviews['date'] = df_reviews['date'].apply(clean_date)

print(df_reviews)

# Converting ratings list of lists to dictionary
def convert_ratings_to_dict(ratings, headers):
    reviews_list = []
    review_dict = {}
    count = 0
    for rating in ratings:
        if rating[0] in headers:
            review_dict[rating[0]] = int(rating[1])
            count += 1
        if count == len(headers):
            reviews_list.append(review_dict)
            review_dict = {}
            count = 0
    return reviews_list

rating_headers = ['Overall', 'Food', 'Service', 'Ambience']

reviews_dicts = convert_ratings_to_dict(all_ratings, rating_headers)
df_ratings = pd.DataFrame(reviews_dicts)
print(df_ratings)

# Combining ratings and reviews into one Dataframe
df_combined = pd.concat([df_reviews, df_ratings], axis=1)

# converting to date 
df_combined['date'] = pd.to_datetime(df_combined['date'], errors='coerce')

print(df_combined.dtypes)

df_combined.head