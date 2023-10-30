#!/bin/bash

SQL="SELECT Book, Page, Subject, Predicate, Object
     FROM df
     WHERE Predicate LIKE '%son%'
     OR Predicate LIKE '%daughter%'
     OR Predicate LIKE '%child%'
     OR Predicate LIKE '%brother%'
     OR Predicate LIKE '%sister%'
     OR Predicate LIKE '%cousin%'
     OR Predicate LIKE '%bastard%'
     OR Predicate LIKE '%father%'
     OR Predicate LIKE '%mother%'
     ORDER BY Subject, Object"

python df_creator.py -f ./data/all_raw_triples.csv -q "${SQL}"

