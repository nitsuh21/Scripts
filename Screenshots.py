
from itertools import count
from selenium import webdriver
from selenium.webdriver.common.by import By
import os 
import csv
from itertools import count

options = webdriver.ChromeOptions()
options.headless=True
driver = webdriver.Chrome(options=options)
driver.get("http://www.google.com/gmail/")

#driver.get_screenshot_as_file(os.getcwd()+"scshots"+'bigtexts3.png')

#fullscreen shot
S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
driver.set_window_size(S('Width'),S('Height'))


import csv
list2 = []
with open('URLs.csv') as file:
    reader = csv.reader(file, delimiter=",")
    for i in reader:
        driver.get('https://undsgn.com/uncode/author/john-doe/')
        print(i[0])

driver.close()

driver.quit()