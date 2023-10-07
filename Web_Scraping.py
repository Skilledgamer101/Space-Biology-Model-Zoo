from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup



    
    

def scrape(url,label1,label2,end):
    non_irradiated = []
    irradiated = []
    # Set up the Selenium WebDriver (specify the path to your WebDriver executable)
    driver = webdriver.Chrome()
    # Navigate to the website
    driver.get(url)

    # Wait for a specific element to be loaded (you can customize this)
    wait = WebDriverWait(driver, 2)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
    # Get the page source (including dynamically loaded content)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table = ""
        # Extract and print the first and second columns
    x=0;
    condition = True
    x=26

    while x>24:
        x=0
        table = soup.find('table', {'class': 'mat-table cdk-table mat-elevation-z8 table-w100'})
        for row in table.find_all('tr'):
          columns = row.find_all('td')
          if len(columns) >= 2:
            first_column = columns[0].get_text().strip()
            second_column = columns[end].get_text().strip()
            if(second_column == label2):
               irradiated.append(first_column)
            else:
               non_irradiated.append(first_column)
            string = first_column+" "+second_column
            x+=1

        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='mat-focus-indicator mat-tooltip-trigger mat-paginator-navigation-next mat-icon-button mat-button-base']")))
            driver.execute_script("arguments[0].setAttribute('style', 'border: 2px solid red;');", button)
            button.click()
        
        except Exception:
            # Button is not clickable, exit the loop
            break
    
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        table = soup.find('table', {'class': 'mat-table cdk-table mat-elevation-z8 table-w100'})
    return non_irradiated,irradiated

data = {}       
data["mouse_noRad"],data["mouse_rad"] = scrape("https://osdr.nasa.gov/bio/repo/data/studies/OSD-466" ,"Ground","Space Flight",12)
data["fish_noRad"],data["fish_rad"] = scrape("https://osdr.nasa.gov/bio/repo/data/studies/OSD-524" ,"non-irradiated","Cobalt-60 gamma radiation",6)
data["plant_noRad"],data["plant_rad"] = scrape("https://osdr.nasa.gov/bio/repo/data/studies/OSD-520","non-irradiated","Cesium-137 gamma radiation",8)
