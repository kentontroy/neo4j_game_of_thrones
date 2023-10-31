# Arya's kills

MATCH (p:Page)-[:HAS_TRIPLE]->(t:Triple)-[:HAS_SUBJECT]->(s:Subject) 
WHERE s.text =~ ".*Arya.*" 
MATCH (t)-[:HAS_PREDICATE]->(a:Predicate)
WHERE a.text =~ ".*kill.*"
RETURN p, t, s, a
