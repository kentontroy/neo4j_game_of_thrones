#!/bin/bash

SQL="SELECT Book, Page, Subject, Predicate, Object
     FROM df
     WHERE Predicate LIKE '%kill%'
     OR Predicate LIKE '%die%'
     OR Predicate LIKE '%fought%'
     OR Predicate LIKE '%battle%'
     OR Predicate LIKE '%stabbed%'
     OR Predicate LIKE '%murder%'"

python df_creator.py -f ./data/all_raw_triples.csv -q "${SQL}"

