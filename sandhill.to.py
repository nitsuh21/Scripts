import csv
import requests
from bs4 import BeautifulSoup
import os

base_url = "https://sandhill.io/feeds"

def main():
    # Check if the file exists
    file_exists = os.path.exists('sandhill.csv')

    # Open file in append mode with newline=''
    with open('sandhill.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        existing_phone_numbers = set()

        # If file doesn't exist, write header
        if not file_exists:
            writer.writeheader()

        for i in range(1, 28):
            page = i
            url = f"{base_url}/?page={page}"
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            content = soup.find('h5', class_="inter")
            print(content)
if __name__ == "__main__":
    main()
