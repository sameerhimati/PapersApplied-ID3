import math, collections


class Node:
    """The Node class is needed to create the tree"""
    def __init__(self):
        self.value = None
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

        feature_values = self.x.loc[values, feature].values # get the feature values (For example, Outlook) = ['Sunny', 'Overcast', 'Rain', 'Sunny', ... etc]

        unique_values = list(set(feature_values)) # get the unique values ['Sunny', 'Overcast', 'Rain']

        feature_entropy = []

        for value in unique_values:
            # Get indices where feature has this value
            value_indices = [values[i] for i in range(len(values)) if self.x.loc[values[i], feature] == value] # A list of indices where the feature value is the same as the value, eg [0, 3, 4, 7...]
            
            # Calculate entropy for this subset
            value_entropy = self._entropy(value_indices) # eg. Entropy for Sunny

            # Get proportion of samples with this value
            value_proportion = len(value_indices) / len(values) # how many Sunny/All Values
            feature_entropy.append(value_entropy * value_proportion) # Sunny's Entropy added to the list

        info_gain = total_entropy - sum(feature_entropy)

        return info_gain
    
    def _best_feature(self, values, features):
        """
        Finds the best feature to split on based on information gain.

        Parameters
        ----------
        values : list of ids
            The list of values to calculate the information gain of.
        
        features : list of column Names

        Returns
        -------
        str
        """
        best_feature = None
        best_info_gain = -1

        for feature in features:
            info_gain = self._information_gain(values, feature)
            if info_gain > best_info_gain:
                best_info_gain = info_gain
                best_feature = feature

        return best_feature
    

    def _build_tree(self, values, features, node):
        """
        Builds the decision tree recursively.

        Parameters
        ----------
        values : list of ids
            The list of values to calculate the information gain of.
        
        features : list of column Names
            The list of features to split on.

        node : Node
            The current node in the decision tree.

        Returns
        -------
        Node
        """
        if not node:
            node = Node()
        
        # Leaf node cases
        if len(set(self.target[i] for i in values)) == 1:
            node.value = self.target[values[0]]  # Class prediction
            return node

        if not features:
            node.value = self.target[values[0]]  # Class prediction
            return node
        
        # Decision node
        best_feature = self._best_feature(values, features)
        node.value = best_feature  # Feature name
        
        unique_values = list(set(self.x[best_feature]))
        new_features = [f for f in features if f != best_feature]
        
        for value in unique_values:
            child = Node()
            child.value = value  # Feature value
            
            # Get subset of data for this feature value
            value_indices = [i for i in values if self.x.loc[i, best_feature] == value]
            
            if value_indices:
                # Create child node for prediction
                prediction_node = self._build_tree(value_indices, new_features, Node())
                child.children.append(prediction_node)
            else:
                # If no examples, create leaf with majority class
                prediction_node = Node()
                prediction_node.value = self.target[values[0]]
                child.children.append(prediction_node)
                
            node.children.append(child)
        
        return node

    def fit(self):
        self.node = self._build_tree(list(range(len(self.x))), self.features, None)

    def print_tree(self, node=None, indent=""):
        if node is None:
            node = self.node
            
        # Print current node
        if node.value in ['Yes', 'No']:  # If it's a prediction
            print(indent + "=> " + str(node.value))  # Use => to mark predictions
        else:
            print(indent + str(node.value))
        
        # Print all children
        for child in node.children:
            print(indent + "├── " + str(child.value))
            # Print child's children with increased indent
            for grandchild in child.children:
                self.print_tree(grandchild, indent + "│   ")