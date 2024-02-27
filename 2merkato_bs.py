import requests
from bs4 import BeautifulSoup

companies_info = []

base_url = "https://www.2merkato.com"

url = f"{base_url}/directory/1/page:1"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

content = soup.find('div', id="listings")

companies = content.find_all('div', class_="row-fluid")

def get_full_detail(link):
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
                        phones.append({"phone_type": phone_type, "phone_number": phone_number})
        return phones

    except requests.exceptions.RequestException as e:
        print(f"Error fetching full phone number for {url}: {e}")
        return None


for company in companies:
    header = company.find('h4')
    if header is not None:
        name = header.text.strip().replace('\n', '')
    
    phone_number = company.find('h5',class_="pull-right")

    if phone_number:  
        link = phone_number.a['href']
        phone_numbers = get_full_detail(link)
        #phone_number = phone_number.text.strip().replace('\n', '')
    #print(phone_numbers)

    companies_info.append({"name": name, "phone_number": phone_numbers}) 

#print(companies_info)
for company in companies_info:
    print("=======")
    print(company)