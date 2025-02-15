


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
        pass
