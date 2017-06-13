#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import csv

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
