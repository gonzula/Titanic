#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter
from sys import stderr

import pprint
import csv
import random

import id3

if __name__ == '__main__':
    with open('train.csv') as f:
        reader = csv.DictReader(f)
        train = list(reader)
    with open('test.csv') as f:
        reader = csv.DictReader(f)
        test = list(reader)

    attrs_to_ignore = {'PassengerId', 'Name', 'Ticket', 'Cabin'}
    class_attr = 'Survived'
    attrs = set(train[0].keys())
    significant_attrs = attrs - set([class_attr]) - attrs_to_ignore

    dataset = train + test

    avg_age = sum(float(p['Age']) for p in dataset if p['Age'])  # sum all ages
    avg_age /= sum(1 for p in dataset if p['Age'])  # divibe by number of available
    avg_age = round(avg_age)

    avg_fare = sum(float(p['Fare']) for p in dataset if p['Fare'])
    avg_fare /= sum(1 for p in dataset if p['Fare'])
    avg_fare = round(avg_fare)

    embarked = Counter(p['Embarked'] for p in dataset)  # Count occurrences
    embarked, _ = embarked.most_common(1)[0]  # Select the most common

    age_interval = 20  # round each 20
    fare_interval = 200
    parch_interval = 4
    for p in dataset:
        p['Age'] = round(float(p['Age'])) if p['Age'] else avg_age
        p['Fare'] = float(p['Fare']) if p['Fare'] else avg_fare
        p['Embarked'] = p['Embarked'] or embarked
        p['Parch'] = int(p['Parch'])
        p['SibSp'] = int(p['SibSp'])
        if class_attr in p:
            p[class_attr] = int(p[class_attr])

        p['Age'] = round(p['Age']/age_interval) * age_interval
        p['Fare'] = round(p['Fare']/fare_interval) * fare_interval
        p['Parch'] = round(p['Parch']/parch_interval) * parch_interval
        p['SibSp'] = round(p['SibSp']/parch_interval) * parch_interval


    tree = id3.ID3(train, significant_attrs, class_attr)
    total = 0
    correct = 0
    print('PassengerId,Survived')
    for row in test:
        o = tree.query(row)
        if class_attr in row:
            e = row[class_attr]
            print(e, o, e==o)
            if e==o:
               correct += 1
            total += 1
        else:
            print(row['PassengerId'], o, sep=',')

    if total:
        print(correct/total, file=stderr)
