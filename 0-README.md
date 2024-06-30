# Restaurant Reviews Sentiment Analysis

# Overview
I have compiled reviews for the restaurant I work at for the past year. My goal is to use the text from the reviews to perform a sentiment analysis to see what are the frequently recurring praise and complaints of customers for both positive and negative reviews.

# Data Collection
Using Python and the BeautifulSoup library, I scraped a year's worth of publicly posted reviews. I pulled the username, date, and review text into a Pandas dataframe and then loaded it to a postgreSQL database. <br>
[data collection and cleaning](https://github.com/aklesitz/rest_reviews/blob/main/getData.py) <br>

# Data Cleaning
The date column pulled from the html was a phrase (either dined 2 days ago or dined on {date}), so I created a function using a regex expression to convert the colummn into a proper date format, then converted it to a datetime data type for insertion into SQL database.

# Database Creation
I used the psycopg library to create a table for SQL storage and populated it with the cleaned dataframe. <br>
[SQL database creation](https://github.com/aklesitz/rest_reviews/blob/main/df_to_postgre.py)