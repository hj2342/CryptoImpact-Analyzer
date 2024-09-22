import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import re

def fetch_crypto_data(coin_id='bitcoin', days=30):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': days,
        'interval': 'daily'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        data = response.json()
        prices = data['prices']
        volume = data['total_volumes']
        market_caps = data['market_caps']

        # Format the data into a DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['volume'] = [v[1] for v in volume]
        df['market_cap'] = [m[1] for m in market_caps]

        return df
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinGecko: {e}")
        return None
    except KeyError as e:
        print(f"Missing expected data in the response: {e}")
        return None

# Fetch cryptocurrency data
crypto_data = fetch_crypto_data('bitcoin', days=100)

if crypto_data is not None:
    # URL of the page to scrape
    url = 'https://indianexpress.com/about/cryptocurrency/'

    try:
        # Send a request to fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all <p> tags that contain timestamps
        timestamp_divs = soup.find_all('p', text=re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b'))

        # Extract and format the dates
        formatted_dates = []
        for div in timestamp_divs:
            timestamp_text = div.get_text()
            # Find the date using regex
            match = re.search(r'(\w+ \d{1,2}, \d{4})', timestamp_text)
            if match:
                date_str = match.group(1)  
                # Convert to desired format
                date_obj = datetime.strptime(date_str, '%B %d, %Y')
                formatted_dates.append(date_obj.strftime('%Y-%m-%d'))  # e.g., "2024-09-11"

        # Remove duplicates and create a DataFrame for the formatted dates
        formatted_dates = list(set(formatted_dates))
        date_df = pd.DataFrame({'date': pd.to_datetime(formatted_dates)})

        # Ensure the 'timestamp' column is in datetime format
        crypto_data['timestamp'] = pd.to_datetime(crypto_data['timestamp'])

        # Merge DataFrames on the date
        combined_df = pd.merge(crypto_data, date_df, left_on='timestamp', right_on='date', how='inner')

        # Calculate the differences
        combined_df['price_diff'] = combined_df['price'].diff()
        combined_df['volume_diff'] = combined_df['volume'].diff()
        combined_df['market_cap_diff'] = combined_df['market_cap'].diff()
        combined_df = combined_df.sort_values('date', ascending=False)  # Sort from most recent to older

        # Display the combined DataFrame with differences
        print(combined_df[['date', 'price', 'price_diff', 'volume', 'volume_diff', 'market_cap', 'market_cap_diff']])

        # Save the combined DataFrame to a CSV file
        combined_df.to_csv('crypto_news_impact_analysis.csv', index=False)

        # User input for a specific date
        user_date = input("Enter a date (YYYY-MM-DD) to check news impact: ")
        if user_date in combined_df['date'].dt.strftime('%Y-%m-%d').values:
            specific_row = combined_df[combined_df['date'] == user_date].iloc[0]
            
            # Determine if the news had a positive or negative impact
            impact = "No Impact"  # Default if no previous day price available
            if not pd.isna(specific_row['price_diff']):
                impact = "Positive Impact" if specific_row['price_diff'] > 0 else "Negative Impact"
            
            print(f"Date: {specific_row['date']}")
            print(f"Price: {specific_row['price']}")
            print(f"Price Difference: {specific_row['price_diff']}")
            print(f"Volume: {specific_row['volume']}")
            print(f"Volume Difference: {specific_row['volume_diff']}")
            print(f"Market Cap: {specific_row['market_cap']}")
            print(f"Market Cap Difference: {specific_row['market_cap_diff']}")
            print(f"Impact of News: {impact}")
        else:
            print("No data available for the entered date.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
