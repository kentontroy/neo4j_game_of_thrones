from dotenv import load_dotenv
from langchain.graphs.networkx_graph import NetworkxEntityGraph
import argparse
import ast
import os
import numpy as np
import pandas as pd
import pandasql as ps
import re

#####################################################################################
# Read triples from file into a dataframe
#####################################################################################
def readTriplesFromFile(filePath: str) -> pd.DataFrame:
  data = []
  with open(filePath, "r") as f:
    book = ""
    if re.search("game_of_thrones", filePath):
      book = "Game Of Thrones"
    elif re.search("a_clash_of_kings", filePath):
      book = "A Clash Of Kings"
    elif re.search("a_storm_of_swords", filePath):
      book = "A Storm Of Swords"
    elif re.search("a_feast_for_crows", filePath):
      book = "A Feast For Crows"
    elif re.search("a_dance_with_dragons", filePath):
      book = "A Dance With Dragons"
    for l in f.readlines():
      line = l.split(":", 1)
      page = line[0].strip()
      triples = ast.literal_eval(line[1].strip())
      for triple in triples:
        subject = triple[0].strip()
        object = triple[1].strip()
        predicate = triple[2].strip()
        data.append([book, page, subject, predicate, object])

  df = pd.DataFrame(data, columns=["Book", "Page", "Subject", "Predicate", "Object"])   
  return df

#####################################################################################
# Save triples in a dataframe to a file
#####################################################################################
def saveTriplesToFile(df: pd.DataFrame, filePath: str):
  df.to_csv(filePath, sep = "|", index=False)

def readTriplesFromDfFile(filePath: str) -> pd.DataFrame:
  df = pd.read_csv(filePath, sep = "|") 
  return df

#####################################################################################
# Get unique predicates
#####################################################################################
def getUniquePredicates(df: pd.DataFrame) -> pd.DataFrame:
  query = f"""SELECT DISTINCT(Predicate) AS predicate
              FROM df 
           """
  return ps.sqldf(query, locals())

#####################################################################################
# Remove undesired subjects and objects 
#####################################################################################
def getTriplesWithoutLabel(df: pd.DataFrame, label: str) -> pd.DataFrame:
  label = label.upper()
  query = f"""SELECT Book, Page, Subject, Predicate, Object
              FROM df 
              WHERE UPPER(Subject) NOT LIKE '%{label}%' AND UPPER(Object) Not LIKE '%{label}%'
              AND UPPER(Predicate) NOT LIKE '%{label}%'
           """
  return ps.sqldf(query, locals())

#####################################################################################
# Get subjects and objects having a label
#####################################################################################
def getTriplesWithLabel(df: pd.DataFrame, label: str) -> pd.DataFrame:
  label = label.upper()
  query = f"""SELECT Book, Page, Subject, Predicate, Object 
              FROM df 
              WHERE UPPER(Subject) LIKE '%{label}%' OR UPPER(Object) LIKE '%{label}%'
           """
  return ps.sqldf(query, locals())


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", type=str, required=True, help="Specify the filename where dataframe was saved")
  parser.add_argument("-l", "--label", type=str, required=False, help="Specify the label of interest")
  parser.add_argument("-p", "--predicate", action="store_true", required=False, help="List the unique predicates")
  args = parser.parse_args()

  df = readTriplesFromDfFile(filePath = args.file)

  if not args.label and not args.predicate:
    print("Incorrect usage: python df_creator.py [-h] to get help on command options")
    exit()

  if args.label and not args.predicate:
    dfQuery = getTriplesWithLabel(df = df, label = args.label)
  elif not args.label and args.predicate:
    dfQuery = getUniquePredicates(df = df)
  elif args.label and args.predicate:
    dfQuery = getTriplesWithLabel(df = df, label = args.label)
    dfQuery = getUniquePredicates(df = dfQuery)
    
  print(dfQuery) 
