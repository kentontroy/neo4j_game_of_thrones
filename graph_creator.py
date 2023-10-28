from characters import characters
from dotenv import load_dotenv
from langchain.graphs.networkx_graph import NetworkxEntityGraph
from negatives import negatives
import argparse
import df_creator as dfCreate
import os
import pandas as pd
import pandasql as ps

if __name__ == "__main__":
  tripleFiles = [
# A Game of Thrones -  Book 1.pdf
    "game_of_thrones_pages_10_109.txt",
    "game_of_thrones_pages_110_159.txt",
    "game_of_thrones_pages_160_209.txt",
    "game_of_thrones_pages_210_259.txt",
    "game_of_thrones_pages_260_309.txt",
    "game_of_thrones_pages_310_359.txt",
    "game_of_thrones_pages_360_409.txt",
    "game_of_thrones_pages_410_459.txt",
    "game_of_thrones_pages_460_509.txt",
    "game_of_thrones_pages_510_552.txt",
# A Clash of Kings - Book 2.pdf
    "a_clash_of_kings_10_109.txt",
    "a_clash_of_kings_110_159.txt",
    "a_clash_of_kings_160_209.txt",
    "a_clash_of_kings_210_259.txt",
    "a_clash_of_kings_260_309.txt",
    "a_clash_of_kings_310_359.txt",
    "a_clash_of_kings_360_409.txt",
    "a_clash_of_kings_411_459.txt",
    "a_clash_of_kings_460_509.txt",
    "a_clash_of_kings_510_559.txt",
    "a_clash_of_kings_560_609.txt",
    "a_clash_of_kings_610_612.txt",
# A Storm of Swords - Book 3.pdf
    "a_storm_of_swords_10_109.txt",
    "a_storm_of_swords_110_159.txt",
    "a_storm_of_swords_160_209.txt",
    "a_storm_of_swords_210_259.txt",
    "a_storm_of_swords_260_309.txt",
    "a_storm_of_swords_310_359.txt",
    "a_storm_of_swords_360_409.txt",
    "a_storm_of_swords_410_459.txt",
    "a_storm_of_swords_460_509.txt",
    "a_storm_of_swords_510_559.txt",
    "a_storm_of_swords_560_609.txt",
    "a_storm_of_swords_610_659.txt",
    "a_storm_of_swords_660_709.txt",
    "a_storm_of_swords_710_759.txt",
    "a_storm_of_swords_760_787.txt",
# A Feast for Crows - Book 4.pdf
    "a_feast_for_crows_10_109.txt",
    "a_feast_for_crows_110_159.txt",
    "a_feast_for_crows_160_209.txt",
    "a_feast_for_crows_210_259.txt",
    "a_feast_for_crows_260_309.txt",
    "a_feast_for_crows_310_359.txt",
    "a_feast_for_crows_360_409.txt",
    "a_feast_for_crows_410_459.txt",
    "a_feast_for_crows_460_509.txt",
    "a_feast_for_crows_510_559.txt",
    "a_feast_for_crows_560_586.txt",
# A Dance With Dragons - Book 5.pdf
    "a_dance_with_dragons_10_109.txt",
    "a_dance_with_dragons_110_209.txt",
    "a_dance_with_dragons_210_309.txt",
    "a_dance_with_dragons_310_409.txt",
    "a_dance_with_dragons_410_509.txt",
    "a_dance_with_dragons_510_609.txt",
    "a_dance_with_dragons_610_709.txt",
    "a_dance_with_dragons_710_809.txt",
    "a_dance_with_dragons_810_909.txt"
  ]

  load_dotenv()
  dfTriples = pd.DataFrame()
  for t in tripleFiles:
    path = os.path.join(os.getenv("TRIPLES_DIR_FILES"), t)
    df = dfCreate.readTriplesFromFile(filePath = path) 
    dfTriples = pd.concat([dfTriples, df], ignore_index=True, axis=0)

# Remove any duplicate triples that were created on the same page
  dfTriples.drop_duplicates(inplace = True)

# Remove undesired words due to hallucinations, NSFW, or unwanted characters" 
  for negative in negatives:
    dfTriples = dfCreate.getTriplesWithoutLabel(df = dfTriples, label = negative)

  path = os.path.join(os.getenv("TRIPLES_DIR_FILES"), "all_raw_triples.csv")
  dfCreate.saveTriplesToFile(df = dfTriples, filePath = path)
  print(dfTriples)
  
