import numpy as np
import pandas as pd
from collections import deque

# generate some data to work with
# define features and target values, these are based on the ID3 Paper
data = {
    'Outlook': ['Sunny', 'Overcast', 'Rain'],
    'Temperature': ['Hot', 'Mild', 'Cool'],
    'Humidity': ['High', 'Normal'],
    'Wind': ['Weak', 'Strong'],
    'Class': ['No', 'Yes']
}

def correctClass(row):
    """
    Determines the class label ('Yes' or 'No') for a given row of data based on 
    predefined conditions involving the 'Outlook', 'Humidity', and 'Wind' features.

    Args:
        row (dict): A dictionary containing feature values for a data point.

    Returns:
        str: 'Yes' if the conditions are met, otherwise 'No'.
    """

    if (row['Outlook'] == 'Overcast') or (row['Outlook'] == 'Sunny' and row['Humidity'] == 'Normal') or (row['Outlook'] == 'Rain' and row['Wind'] == 'Weak'):
        return 'Yes'
    else:
        return 'No'

# create an empty dataframe to hold the data
data_random = pd.DataFrame(columns=data.keys())
df = pd.DataFrame(columns=data.keys())

np.random.seed(42)
# create 1000 instances of random classes
for i in range(1000):
    row = {}
    for key in data.keys():
        row[key] = np.random.choice(list(data[key]), 1)[0]
    data_random.loc[i] = row

# create 1000 instances of Non Random classes
for i in range(1000):
    row = {}
    for key in df.keys():
        if key == 'Class':
            row[key] = correctClass(row) # apply the correctClass function
            continue # continue to the next iteration
        row[key] = np.random.choice(data[key])
    df.loc[i] = row

# save to csv
data_random.to_csv('noisy.csv', index=False)
df.to_csv('clean.csv', index=False)