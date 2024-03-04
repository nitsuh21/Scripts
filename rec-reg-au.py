import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.rec-registry.gov.au/rec-registry/app/calculators/swh-stc-calculator"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

form = soup.find('form')

select_element = soup.find('select')

if select_element:
    option_elements = select_element.find_all('option')
    print("Option elements:", option_elements)

    # Extract option values
    option_values = [option.get('value') for option in option_elements]

    print("Option values:", option_values)
else:
    print("No select element found on the page.")
    
input_elements = form.find_all('input')  

data = {}
for input_element in input_elements:
    input_name = input_element.get('name')
    if input_name:
        # Fill input fields with your data
        data[input_name] = 'your input data' 