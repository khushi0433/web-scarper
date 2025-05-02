import argparse
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd

def read_csv_file(csv_path):
    try:
        print(f"Reading CSV file: {csv_path}")
        with open(csv_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print("CSV file content:\n", content)  # Print the raw content of the file
            
        df = pd.read_csv(csv_path)
        
        # Check if the file is empty
        if df.empty:
            print("CSV is empty!")
        else:
            print("CSV Loaded successfully!")
            print(df.head())  # Show the first few rows to check the data
        return df
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Scrape text from a web page using a CSS selector.")
    parser.add_argument("--url", required=False, help="URL of the web page to scrape")
    parser.add_argument("--selector", required=False, help="CSS selector to extract content")
    parser.add_argument("--json", required=False, help="URL for JSON data")
    parser.add_argument("--output", required=False, help="Path to save the scraped content")
    parser.add_argument("--csv", required=False, help="Path to a local CSV file to parse")
    
    args = parser.parse_args()

    # CSV parsing logic
    if args.csv:
        print(f"Reading CSV file: {args.csv}")
        df = read_csv_file(args.csv)
        # If you want to perform further actions with CSV data, you can add them here

    # Web scraping logic (for --url and --selector)
    if args.url and args.selector:
        print(f"Fetching URL: {args.url}")
        try:
            response = requests.get(args.url)
            response.raise_for_status()
        except RequestException as e:
            print(f"Network error: {e}")
            return

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            elements = soup.select(args.selector)
            if elements:
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as file:
                        for element in elements:
                            file.write(element.get_text() + "\n")
                    print(f"Saved to {args.output}")
                else:
                    for element in elements:
                        print(element.get_text(strip=True))
            else:
                print("No elements found for the given selector.")
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
    
    # JSON fetching logic (for --json)
    if args.json:
        print(f"Fetching JSON data from {args.json}")
        try:
            response = requests.get(args.json)
            response.raise_for_status()
            data = response.json()
            print("JSON data fetched successfully!")
            print(data)  # You can process the data as needed
        except RequestException as e:
            print(f"Network error: {e}")
        except ValueError as e:
            print(f"Error decoding JSON: {e}")

if __name__ == "__main__":
    main()
