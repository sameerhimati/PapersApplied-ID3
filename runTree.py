from createTree import DecisionTree
import pandas as pd
import numpy as np

df = pd.read_csv('clean.csv')
features = ['Outlook', 'Temperature', 'Humidity', 'Wind']

x = df[features]
y = df['Class']

tree = DecisionTree(x, features, y)
tree.fit()
tree.print_tree()