
########################################################

filePath = "./data/all_raw_triples.csv"
with open(filePath, "r") as f:        
  i = 0
  lines = f.readlines()
  for line in lines:
    print(line)
    i += 1
    if i == 1:
      continue
    if len(line.split("|")) > 5:
      print("Found bad line")
      break

    bookName =  line.split("|")[0]
    pageNum =   line.split("|")[1]
    subject =   line.split("|")[2]
    predicate = line.split("|")[3] 
    object =    line.split("|")[4]


