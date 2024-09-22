# Crypto News Impact Analysis

This project analyzes the impact of news on cryptocurrency prices by combining data from CoinGecko and web-scraped dates from a news website.

## Features

- **Fetch Cryptocurrency Data**: Retrieves historical price, volume, and market cap data for a specified cryptocurrency.
- **Web Scraping**: Extracts dates from a news website to analyze potential impacts on cryptocurrency prices.
- **Data Merging**: Combines cryptocurrency data with scraped dates to perform analysis.
- **Impact Analysis**: Calculates price, volume, and market cap differences to assess news impact.
- **CSV Export**: Saves the analysis results to a CSV file.

## Requirements

- Python 3.x
- Libraries: `requests`, `pandas`, `datetime`, `BeautifulSoup`, `re`

## Installation

1. Clone the repository.
2. Install required libraries:
   ```bash
   pip install requests pandas beautifulsoup4
   ```

## Usage

1. **Fetch Cryptocurrency Data**:
   - Modify the `fetch_crypto_data` function to specify the cryptocurrency and number of days.

2. **Web Scraping**:
   - The script scrapes dates from a specified URL using BeautifulSoup.

3. **Run the Analysis**:
   - Execute the script to fetch data, merge datasets, and calculate differences.
   - The results are printed and saved as `crypto_news_impact_analysis.csv`.

4. **Check News Impact**:
   - Enter a date in the format `YYYY-MM-DD` to check if news had an impact on that day.

## Code Explanation

- **fetch_crypto_data**: Retrieves data from CoinGecko API and formats it into a DataFrame.
- **Web Scraping**: Uses BeautifulSoup to extract dates from `<p>` tags containing timestamps.
- **Data Merging**: Merges crypto data with formatted dates and calculates differences.
- **Impact Calculation**: Determines if news had a positive or negative impact based on price differences.

## Example

```python
crypto_data = fetch_crypto_data('bitcoin', days=100)
# Web scrape dates and merge with crypto data...
```

## Error Handling

The script includes error handling for network requests and missing data scenarios.

