import math, collections


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
        
        if len(set(self.target[i] for i in values)) == 1: # if all values are the same
            node.value = self.target[values[0]]
            return node

        if len(features) == 0: # if there are no more features to split on
            node.value = self.target[values[0]] # set the value to the most common target value
            return node
        
        best_feature = self._best_feature(values, features) # find the best feature to split on
        node.value = best_feature # set the value to the best feature

        unique_values = list(set(self.x[i][best_feature] for i in values)) # get the unique values of the best feature, for Outlook we have ['Sunny', 'Overcast', 'Rain']
        
        for value in unique_values:
            # Get indices where feature has this value
            child = Node()
            child.value = value
            node.children.append(child)

            value_indices = [values[i] for i in range(len(self.x)) if self.x[i][best_feature] == value] # A list of indices where the feature value (For example, Outlook) 
                                                                                                        # is the same as the value (For example, Sunny), eg [0, 3, 4, 7...]

            if value_indices:
                if features and best_feature in features:
                    new_features = features.remove(best_feature) # remove the best feature from the list of features

                child.next = self._build_tree(value_indices, new_features, child) # recursively build the tree for this subset
            
            else:
                child.next = Node()
                child.next.value = self.target[values[0]] # set the value to the most common target value
                print('Done')

        return node

    def fit(self):
        self.node = self._build_tree(list(range(len(self.x))), self.features, None)
        print('Done')
    

    def print_tree(self):
        if not self.node:
            return
        
        queue = collections.deque([self.node])
        while queue:
            node = queue.popleft()
            print(node.value)
            if node.children:
                for child in node.children:
                    print('->', child.value)
                    queue.append(child.next)

            elif node.next:
                print('->', node.next.value)