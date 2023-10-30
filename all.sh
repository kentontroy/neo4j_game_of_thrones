#!/bin/bash

SQL="SELECT Book, Page, Subject, Predicate, Object
     FROM df"

python df_creator.py -f ./data/all_raw_triples.csv -q "${SQL}"

