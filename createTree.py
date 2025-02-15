import math


class Node:
    """The Node class is needed to create the tree"""
    def __init__(self):
        self.value = None
        self.next = None
        self.children = []


class DecisionTree:
    def __init__(self, x, features, target): # features = ['Outlook', 'Temperature', 'Humidity', 'Wind']; # target = ['Class']
        self.x = x
        self.features = features
        self.target = target
        self.node = None
        self.entropy = []
        for i in range(len(self.target)): # calculate initial entropy
            self.entropy.append(i) # list of numbers 0 to len(target)
        
        self.entropy = self._entropy(self.entropy) 

    def _entropy(self, values):
        """
        Calculates the entropy of the given values.

        Entropy is a measure of the amount of uncertainty or randomness in a set of values.
        The entropy of a set of values is calculated as the negative sum of the probability
        of each value multiplied by the logarithm of the probability of the value.

        Parameters
        ----------
        values : list of ids
            The list of values to calculate the entropy of.

        Returns
        -------
        float
        """
        y = [self.target[i] for i in values] # get the target values (Yes or No) = ['Yes', 'Yes', 'No', 'Yes', ... etc]

        target_values = [y.count(classes) for classes in set(y)] # count the number of times each class appears in the target values {'Yes': 510, 'No': 490}

        if sum(target_values) == 0: # if all values are the same
            return 0
        
        entropy = sum([-classes/len(y) * math.log(classes/len(y), 2) for classes in target_values]) # calculate the entropy based on the formula 

        return entropy

    def _information_gain(self, values, feature):
        """
        Calculates the information gain for a given feature.

        Information gain is a measure of how much information can be gained when
        a decision is made based on the values.

        Parameters
        ----------
        values : list of ids
            The list of values to calculate the information gain of.

        Returns
        -------
        float
        """
        total_entropy = self._entropy(values)

        feature_values = [self.x[i][feature] for i in values] # get the feature values (For example, Outlook) = ['Sunny', 'Overcast', 'Rain', 'Sunny', ... etc]

        unique_values = list(set(feature_values)) # get the unique values ['Sunny', 'Overcast', 'Rain']

        feature_entropy = []

        for value in unique_values:
            # Get indices where feature has this value
            value_indices = [values[i] for i in range(len(feature_values)) if feature_values[i] == value] # A list of indices where the feature value is the same as the value, eg [0, 3, 4, 7...]
            
            # Calculate entropy for this subset
            value_entropy = self._entropy(value_indices) # eg. Entropy for Sunny

            # Get proportion of samples with this value
            value_proportion = len(value_indices) / len(values) # how many Sunny/All Values
            feature_entropy.append(value_entropy * value_proportion) # Sunny's Entropy added to the list

        info_gain = total_entropy - sum(feature_entropy)

        return info_gain