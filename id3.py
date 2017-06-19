#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from sys import float_info
from collections import Counter
from math import log2

from sys import stderr

class ID3:
    def __init__(self, dataset, attrs, class_attr):
        self.dataset = dataset
        self.attrs = attrs
        self.class_attr = class_attr

        self.tree = self._id3(dataset, attrs, class_attr)

    @staticmethod
    def _H(probs):
        return -sum(p * log2(p) for p in probs if p > 0)

    @staticmethod
    def _H_S(dataset, class_attr):
        classes = set(row[class_attr] for row in dataset)
        probs = []
        for c in classes:
            subset = (row for row in dataset if row[class_attr] == c)
            probs.append(sum(1 for row in subset))
        probs = [p/sum(probs) for p in probs]

        return ID3._H(probs)

    @staticmethod
    def _GI(dataset, attr, class_attr):
        E_S = ID3._H_S(dataset, class_attr)

        options = set(row[attr] for row in dataset)
        fractions = []
        E_S_A = []

        for o in options:
            subset = [row for row in dataset if row[attr] == o]
            fractions.append(sum(1 for row in subset))

            E_S_A.append(ID3._H_S(subset, class_attr))
        fractions = [f/sum(fractions) for f in fractions]

        return E_S - sum(f * e for f, e in zip(fractions, E_S_A))

    def _id3(self, dataset, attrs, class_attr):
        root = {}

        information_gain = {}
        for attr in attrs:
            information_gain[attr] = ID3._GI(dataset, attr, class_attr)

        selected_attr = max(
                (attr for attr in information_gain),
                key=lambda attr: information_gain[attr]
                )

        if abs(ID3._H_S(dataset, class_attr)) < float_info.epsilon:  # H_S == 0
            try:
                root['class'] = dataset[0][class_attr]
            except IndexError as e:
                root['class'] = 0
        elif abs(max(information_gain.values())) < float_info.epsilon:
            classes = set(row[class_attr] for row in dataset)
            occurrences = Counter(row[class_attr] for row in dataset)
            root['class'], _ = occurrences.most_common(1)[0]
        else:
            root['attr'] = selected_attr
            root['possibilities'] = set(row[selected_attr] for row in self.dataset)
            root['children'] = {}

            for p in root['possibilities']:
                subset = [row for row in dataset if row[selected_attr] == p]
                root['children'][p] = self._id3(subset, attrs, class_attr)

        return root


    def query(self, query, node=None):
        node = node or self.tree

        if node.get('class', None) is not None:
            return node['class']

        value = query[node['attr']]
        print(node['attr'], query[node['attr']], file=stderr)
        return self.query(query, node['children'][value])
