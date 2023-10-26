import argparse
import requests
from timeit import default_timer as timer

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-u", "--url", type=str, required=True, help="Specify the model endpoint URL")
  parser.add_argument("-p", "--prompt", type=str, required=True, help="Specify the prompt string")
  parser.add_argument("-s", "--streaming", type=str, required=False, help="Stream the results")
  args = parser.parse_args()

  if args.url and args.prompt:
    if args.streaming:
      endpoint = args.url + "/llm/streaming" 
    else:
      endpoint = args.url + "/llm"

  start = timer()

  res = requests.post(endpoint, json={"prompt": args.prompt})
  res.raise_for_status()
    
  for chunk in res.iter_content(chunk_size=None, decode_unicode=True):
    chunk = chunk.replace("data:", "")
    print(chunk, end="")

  print(f"\n{timer() - start} seconds elapsed\n") 
