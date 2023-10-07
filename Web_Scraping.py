from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


# Set up the Selenium WebDriver (specify the path to your WebDriver executable)
driver = webdriver.Chrome()

# Navigate to the website
url = "https://osdr.nasa.gov/bio/repo/data/studies/OSD-524"  # Replace with the URL of the dynamically loaded website
driver.get(url)

# Wait for a specific element to be loaded (you can customize this)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))
data_files = []
# Get the page source (including dynamically loaded content)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
table = soup.find('table', {'class': 'mat-table cdk-table mat-elevation-z8 table-w100'})
    # Extract and print the first and second columns
x=0;
while table:
    print(table)
    for row in table.find_all('tr'):
      columns = row.find_all('td')
      if len(columns) >= 2:
        first_column = columns[0].get_text().strip()
        second_column = columns[6].get_text().strip()
        
        string = first_column+" "+second_column
        data_files.append(string)
        x+=1
        print(x)
    for string in data_files:
       print(string)
    button = soup.find('button', {'class': 'mat-focus-indicator mat-tooltip-trigger mat-paginator-navigation-next mat-icon-button mat-button-base', 'aria-label': 'Next page'})
    button.click()
    table = soup.find('table', {'class': 'mat-table cdk-table mat-elevation-z8 table-w100'})

# Close the WebDriver
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Now you can use BeautifulSoup to extract information from the parsed HTML
# For example:
# data = soup.find('div', {'class': 'your-class'})