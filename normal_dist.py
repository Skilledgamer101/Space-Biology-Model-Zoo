import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm  # Import the normal distribution module
import parse_json


# Dictionary with keys as labels and values as the data values
mice_basal_dict = parse_json.mice_basal_data
mice_space_dict = parse_json.mice_space_data
zebrafish_basal_dict = parse_json.zebrafish_basal_data
zebrafish_space_dict = parse_json.zebrafish_space_data
plants_basal_dict = parse_json.plants_basal_data
plants_space_dict = parse_json.plants_space_data

dict_list = [mice_basal_dict, mice_space_dict, zebrafish_basal_dict, zebrafish_space_dict, plants_basal_dict, plants_space_dict]


# Loop through key value pairs and create normal distribution
# Plot for every key:value pair of every dictionary
'''
for i in range(len(dict_list)):
    for key, values in dict_list[i].items():
        # Mean and standard deviation for current key's data
        mean = np.mean(values)
        std_dev = np.std(values)
        
        # Data points for normal distribution (perfect normal distribution)
        num_samples = 1000  # Number of data points to generate
        generated_data = np.random.normal(mean, std_dev, num_samples)
        
        # Histogram for the generated data
        # Create a range of x values for the normal distribution curve
        x_range = np.linspace(min(generated_data), max(generated_data), 100)

        # Calculate the PDF values for the normal distribution
        pdf_values = norm.pdf(x_range, mean, std_dev)

        # Plot the normal distribution curve as a line
        plt.plot(x_range, pdf_values, 'r-', label='Normal Distribution')

        plt.xlabel('Value')
        plt.ylabel('Probability Density')
        plt.hist(generated_data, bins=65, density=True, alpha=0.6, label='Generated Data')
        plt.title(f'Normal Distribution Plot for {key}')
        plt.legend()
        plt.show()
'''
# Separability metric

def separability(dict1, dict2):
    keys_list = list(dict1.keys())
    difference = []
    for i in range(4):
        key_at_index = keys_list[i]
        value_dict1 = dict1[key_at_index] # Should be of type list
        value_dict2 = dict2[key_at_index] # Should be of type list
        
        # Mean & std for both dictionaries 
        mean_dict1 = np.mean(value_dict1)
        std_dict1 = np.std(value_dict1)
        mean_dict2 = np.mean(value_dict2)
        std_dict2 = np.std(value_dict2)
        
        # Class Separability --> P1(mean1,std1) and P2(mean2,std2) --> separability is (mean2-mean1)/(std1*std2)
        separability = (mean_dict2-mean_dict1)/(std_dict1*std_dict2)
        difference.append(separability)
        
    return difference

mice_difference = separability(mice_basal_dict,mice_space_dict)
zebra_difference = separability(zebrafish_basal_dict,zebrafish_space_dict)
plant_difference = separability(plants_basal_dict,plants_space_dict)

for i in range(4):
    print(f"The difference of key{i} is {mice_difference[i]} ")
    print(f"The difference of key{i} is {zebra_difference[i]} ")
    print(f"The difference of key{i} is {plant_difference[i]} ")



