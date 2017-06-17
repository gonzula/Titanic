#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter

import pprint
import csv

if __name__ == '__main__':
    with open('train.csv') as f:
        reader = csv.DictReader(f)
        train = list(reader)
    with open('test.csv') as f:
        reader = csv.DictReader(f)
        test = list(reader)

    attrs_to_ignore = set(['PassengerId', 'Name', 'Ticket', ])
    class_attr = set(['Survived'])
    attrs = set(train[0].keys())
    significant_attrs = attrs - class_attr - attrs_to_ignore
    pprint.pprint(train[:20])

    dataset = train + test

    avg_age = sum(float(p['Age']) for p in dataset if p['Age'])  # sum all ages
    avg_age /= sum(1 for p in dataset if p['Age'])  # divibe by number of available
    avg_age = round(avg_age)

    avg_fare = sum(float(p['Fare']) for p in dataset if p['Fare'])
    avg_fare /= sum(1 for p in dataset if p['Fare'])
    avg_fare = round(avg_fare)

    embarked = Counter(p['Embarked'] for p in dataset)  # Count occurrences
    embarked, _ = embarked.most_common(1)[0]  # Select the most common

    for p in dataset:
        p['Age'] = round(float(p['Age'])) if p['Age'] else avg_age
        p['Fare'] = float(p['Fare']) if p['Fare'] else avg_fare

        if not p['Embarked']:
            p['Embarked'] = embarked
        del p['Cabin']  # del cabin because there aren't information enough


