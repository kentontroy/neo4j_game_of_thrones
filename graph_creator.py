from neo4j import GraphDatabase

#URI = "bolt://game_of_thrones_neo4j:7687"
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "cloudera")

driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()

########################################################

import df_creator as dfCreate
import pandas as pd

filePath = "./data/all_raw_triples.csv"
pd.options.display.max_rows = 100
df = dfCreate.readTriplesFromDfFile(filePath = filePath)
sql = """SELECT Book, Page, Subject, Predicate, Object
         FROM df
      """
dfQuery = dfCreate.runSql(df = df, sql = sql)
print(dfQuery)

########################################################
from typing import Tuple

books = [
  "Game Of Thrones", 
  "A Clash Of Kings", 
  "A Storm Of Swords",  
  "A Feast For Crows",
  "A Dance With Dragons"
]

def _create_book_(tx, book):
  result = tx.run("MERGE (b:Book { name: $book }) RETURN b", book=book)
  return result

def _create_book_to_page_(tx, data: Tuple[str, str, str, str, str]):
  cypher =  f"MATCH (b:Book) WHERE b.name = '{data[0]}' "
  cypher +=  "MERGE (p:Page { number: $pageNum, book: b.name }) "
  cypher +=  "MERGE (b)-[r:HAS_CONTENT_ON]->(p) "
  cypher +=  "RETURN b,r,p"
  result = tx.run(cypher, pageNum=data[1])
  return result

def _create_page_to_triple_(tx, data: Tuple[str, str, str, str, str]):
  cypher =  "MERGE (p:Page { number: $pageNum, book: $bookName }) " 
  cypher += "MERGE (t:Triple { text: $fragment }) "
  cypher += "MERGE (p)-[r:HAS_TRIPLE]->(t) "
  cypher += "RETURN p,r,t"
  fragment = data[2] + " " + data[3] + " " + data[4] 
  result = tx.run(cypher, pageNum=data[1], bookName=data[0], fragment=fragment)
  return result

def _create_triple_to_subject_(tx, data: Tuple[str, str, str, str, str]):
  cypher =  "MERGE (t:Triple { text: $fragment }) "
  cypher += "MERGE (s:Subject { text: $subject }) "
  cypher += "MERGE (t)-[r:HAS_SUBJECT]->(s) "
  cypher += "RETURN t,r,s"
  fragment = data[2] + " " + data[3] + " " + data[4] 
  result = tx.run(cypher, fragment=fragment, subject=data[2])
  return result

def _create_triple_to_predicate_(tx, data: Tuple[str, str, str, str, str]):
  cypher =  "MERGE (t:Triple { text: $fragment }) "
  cypher += "MERGE (p:Predicate { text: $predicate }) "
  cypher += "MERGE (t)-[r:HAS_PREDICATE]->(p) "
  cypher += "RETURN t,r,p"
  fragment = data[2] + " " + data[3] + " " + data[4] 
  result = tx.run(cypher, fragment=fragment, predicate=data[3])
  return result

def _create_triple_to_object_(tx, data: Tuple[str, str, str, str, str]):
  cypher =  "MERGE (t:Triple { text: $fragment }) "
  cypher += "MERGE (o:Object { text: $object }) "
  cypher += "MERGE (t)-[r:HAS_OBJECT]->(o) "
  cypher += "RETURN t,r,o"
  fragment = data[2] + " " + data[3] + " " + data[4] 
  result = tx.run(cypher, fragment=fragment, object=data[4])
  return result


with driver.session() as session:
  for book in books:
    result = session.execute_write(_create_book_, book)
    print(result)

  with open(filePath, "r") as f:        
    i = 0
    lines = f.readlines()
    for line in lines:
      print(line)
      i += 1
      if i == 1:
        continue
      bookName =  line.split("|")[0]
      pageNum =   line.split("|")[1]
      subject =   line.split("|")[2]
      predicate = line.split("|")[3] 
      object =    line.split("|")[4]
      result = session.execute_write(_create_book_to_page_, (bookName, pageNum, subject, predicate, object))
      print(result)
      result = session.execute_write(_create_page_to_triple_, (bookName, pageNum, subject, predicate, object))
      print(result)
      result = session.execute_write(_create_triple_to_subject_, (bookName, pageNum, subject, predicate, object))
      print(result)
      result = session.execute_write(_create_triple_to_predicate_, (bookName, pageNum, subject, predicate, object))
      print(result)
      result = session.execute_write(_create_triple_to_object_, (bookName, pageNum, subject, predicate, object))
      print(result)


