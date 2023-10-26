from dotenv import load_dotenv
from langchain.graphs.networkx_graph import NetworkxEntityGraph
import argparse
import ast
import os
import numpy as np
import pandas as pd
import pandasql as ps

#####################################################################################
# Read triples from file into a dataframe
#####################################################################################
def readTriplesFromFile(filePath: str) -> pd.DataFrame:
  data = []
  with open(filePath, "r") as f:
    for l in f.readlines():
      line = l.split(":", 1)
      page = line[0].strip()
      triples = ast.literal_eval(line[1].strip())
      subject = triples[0][0].strip()
      object = triples[0][1].strip()
      predicate = triples[0][2].strip()
      data.append([page, subject, object, predicate])
  df = pd.DataFrame(data, columns=["Page", "Subject", "Object", "Predicate"])   
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
# Get subjects and objects having a label
#####################################################################################
def getTriplesWithLabel(df: pd.DataFrame, label: str) -> pd.DataFrame:
  query = f"""SELECT Page, Subject, Object, Predicate 
              FROM df 
              WHERE Subject LIKE '{label}%' OR Object LIKE '{label}%'
           """
  return ps.sqldf(query, locals())


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", type=str, required=True, help="Specify the filename containing the triples")
  parser.add_argument("-l", "--label", type=str, required=False, help="Specify the label of interest")
  parser.add_argument("-p", "--predicate", action="store_true", required=False, help="List the unique predicates")
  args = parser.parse_args()

  df = readTriplesFromFile(filePath = args.file)

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
