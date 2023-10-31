# Cite everything explicity using the schema

MATCH (b:Book)-[:HAS_CONTENT_ON]->(p:Page)
MATCH (p:Page)-[:HAS_TRIPLE]->(t:Triple)
MATCH (t)-[:HAS_SUBJECT]->(s:Subject)
MATCH (t)-[:HAS_PREDICATE]->(a:Predicate)
MATCH (t)-[:HAS_OBJECT]->(o:Object)
RETURN b,p,t,s,a,o

# Arya's kills

MATCH (p:Page)-[:HAS_TRIPLE]->(t:Triple)-[:HAS_SUBJECT]->(s:Subject) 
WHERE s.text =~ ".*Arya.*" 
MATCH (t)-[:HAS_PREDICATE]->(a:Predicate)
WHERE a.text =~ ".*kill.*"
RETURN p, t, s, a
