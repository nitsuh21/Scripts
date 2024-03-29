import csv
import requests
from bs4 import BeautifulSoup
import os

base_url = "https://www.2merkato.com"

def get_full_detail(link, company_name, existing_phone_numbers):
    try:
        url = f"{base_url}/{link}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', class_='table table-condensed')
        phones = []
        if table:
            rows = table.find_all('tr')
            valid_tr_elements = [tr for tr in rows if tr.find('td') is not None]
            for row in valid_tr_elements:
                row_elements = row.find_all('td')
                if len(row_elements) == 2:
                    if row_elements[0].b.text in ["Phone", "Phone 2", "Mobile", "Mobile 2", "Phone 3", "Mobile 3"]:
                        phone_type = row_elements[0].text
                        phone_number = row_elements[1].text
                        # Check if phone number for this company already exists
                        if (company_name, phone_number) not in existing_phone_numbers:
                            phones.append({"phone_type": phone_type, "phone_number": phone_number})
                            existing_phone_numbers.add((company_name, phone_number))  # Add to existing phone numbers
        return phones

    except requests.exceptions.RequestException as e:
        print(f"Error fetching full phone number for {url}: {e}")
        return None


def main():
    # Check if the file exists
    file_exists = os.path.exists('companies_data.csv')

    # Open file in append mode with newline=''
    with open('exporters_companies_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'phone_type', 'phone_number','website']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        existing_phone_numbers = set()

        # If file doesn't exist, write header
        if not file_exists:
            writer.writeheader()

        url = f"{base_url}/directory/1/"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        content = soup.find('ul', class_="pad10")
        directory_links = []
        for directory in content:
            directory_links.append(f"{base_url}/{directory.a['href']}")
        
        for link in directory_links:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html.parser')
            content = soup.find('div', id="listings")
            companies = content.find_all('div', class_="row-fluid")

            if content:
                    companies = content.find_all('div', class_="row-fluid")
                    
                    for company in companies:
                        header = company.find('h4')
                        website_link = company.find('a', class_="pull-right")
                        if website_link:
                            website = website_link.get('href')
                        else:
                            website = ''
                        print(website)
                        if header is not None:
                            name = header.text.strip().replace('\n', '')
                            link = header.a['href']
                            phone_details = get_full_detail(link, name, existing_phone_numbers)
                            for phone in phone_details:
                                try:
                                    print(f"Writing to file: {name} - {phone['phone_number']} - {website}")
                                    writer.writerow({'name': name, 'phone_type': phone['phone_type'], 'phone_number': phone['phone_number'], 'website':website})
                                    csvfile.flush()
                                except Exception as e:
                                    print(f"Error writing to file: {e}")
                                    print("=====================================")
                                    print(f"Name: {name}")
                                    print(f"Phone: {phone['phone_number']}")
                                    print(f"Phone Type: {phone['phone_type']}")
                
            else:
                print(f"No content for page")

if __name__ == "__main__":
    main()