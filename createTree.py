


class Node:
    """The Node class is needed to create the tree"""
    def __init__(self):
        self.value = None
        self.next = None
        self.children = []


class DecisionTree:
    def __init__(self, input_df, features, target):
        self.df = input_df
        self.features = features
        self.target = target
        self.node = None
        self.entropy = self._entropy([])

    def _entropy(self, values):
        """
        Calculates the entropy of the given values.

        Entropy is a measure of the amount of uncertainty or randomness in a set of values.
        The entropy of a set of values is calculated as the negative sum of the probability
        of each value multiplied by the logarithm of the probability of the value.

        Parameters
        ----------
        values : list of str
            The list of values to calculate the entropy of.

        Returns
        -------
        float
        """
        pass
