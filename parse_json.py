import json
from collections import defaultdict
import pprint



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
    x=0
    condition = True
    x=26

    while x>24:
        x=0
        table = soup.find('table', {'class': 'mat-table cdk-table mat-elevation-z8 table-w100'})
        for row in table.find_all('tr'):
          columns = row.find_all('td')
          if len(columns) >= 2:
            first_column = columns[1].get_text().strip()
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
# source is json file, addition is the string needed to be added at end of samples,
# basal is the list of control sample names, space is list of space sample names
def main(source, addition: str, basal: list, space: list):

    # define a function which searches in stats for specific values from a list of specimens (preferably of the same type)
    def avg(samples: list, addition: str):
        dataset = defaultdict(list)

        for sample in samples:
            sample1, sample2 = sample, sample
            # addition is HRremoved_raw for mice, raw for zebrafish
            sample1 += ("_R1_" + addition)
            sample2 += ("_R2_" + addition)
            dataset['percent_gc'].extend([stats[sample1]['percent_gc'], stats[sample2]['percent_gc']])
            dataset['percent_at'].extend([100 - stats[sample1]['percent_gc'], 100 - stats[sample2]['percent_gc']])
            dataset['percent_duplicates'].extend([stats[sample1]['percent_duplicates'], stats[sample2]['percent_duplicates']])
            dataset['total_sequences'].extend([stats[sample1]['total_sequences'], stats[sample2]['total_sequences']])

        # samples list only has one sample name but stats hashmap has 2 data points for each sample!
        # avg_percent_gc = round(percent_gc / (len(samples) * 2), 2)
        # avg_percent_at = round(percent_at / (len(samples) * 2), 2)
        # avg_duplicates = round(percent_duplicates / (len(samples) * 2), 2)    
        # avg_sequence_length = round(sequence_length / (len(samples) * 2), 2)    

        # print(f"The average percent GC of {type_samples} is {avg_percent_gc}\nThe average percent duplicates of {type_samples} is {avg_duplicates}")
        # return avg_percent_gc, avg_duplicates
        return dataset

    with open(source, 'r') as file:
        source_data = json.load(file)
        # data466 is a hashmap
        stats = source_data["report_general_stats_data"][0]
        
        # stats gives hashmap of specimen : another hashmap with key 'percent_gc'
        # list of all basal gc values
        basal_data = avg(basal, addition)
        space_data = avg(space, addition)
        
    return basal_data, space_data

mice_basal_data, mice_space_data = main(r'C:\Users\ronav\OneDrive\Documents\Python\Model_Zoo\NasaTime\OSD-466.json', 'HRremoved_raw', data["mouse_noRad"], data["mouse_rad"])
zebrafish_basal_data, zebrafish_space_data = main(r'C:\Users\ronav\OneDrive\Documents\Python\Model_Zoo\NasaTime\OSD-524.json', 'raw', data["fish_noRad"], data["fish_rad"])
plants_basal_data, plants_space_data = main(r'C:\Users\ronav\OneDrive\Documents\Python\Model_Zoo\NasaTime\OSD-520.json', 'raw', data["plant_noRad"], data["plant_rad"])
print("Mice basal data")
pprint.pprint(mice_basal_data)
print("Mice space data")

pprint.pprint(mice_space_data)
print("Zebrafish basal data")

pprint.pprint(zebrafish_basal_data)
print("Zebrafish space data")

pprint.pprint(zebrafish_space_data)
print("Plants basal data")

pprint.pprint(plants_basal_data)
print("Plants space data")

pprint.pprint(plants_space_data)




    # def difference(value, type_value):
    #     if value > 0:
    #         print(f"The percentage of {type_value} after going to space is GREATER than before by an amount of {round(abs(value), 2)}")
    #     elif value < 0:
    #         print(f"The percentage of {type_value} after going to space is LESS than before by an amount of {round(abs(value), 2)}")
    #     else:
    #         print(f"The percentage of {type_value} after going to space is SAME as before.")

    # difference(difference_gc, "GC")
    # difference(difference_duplicates, "duplicates")



    # for sample in basal:
    #     sample += "_HRremoved_raw"
    #     # get details of each specific sample
    #     # details is a hashmap
    #     details = stats[sample]
    #     percent_gc = details['percent_gc']
    #     print(f"The percent GC of {sample} is {percent_gc}")
    # # for i in stats:
    # #     # each element
    # #     print(i)
    # #     print('\n\n')
    # # spec_stats = stats["RR10_FCS_BSL_WT_B1_R1_HRremoved_raw"]
    # # print(json.dumps(spec_stats, indent=4))