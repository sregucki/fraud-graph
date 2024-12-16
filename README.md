# Fraud Detection Graph

## Requirements
 - Docker
 - Python 3
 - Git LFS
 - Bash

UNIX systems only!

## Copy CSV files to neo4j/import

```bash
sudo cp data/*.csv ./neo4j/import/
```

## Commands for creating the graph
```cypher
LOAD CSV WITH HEADERS FROM 'file:///accounts.csv' AS row FIELDTERMINATOR ','
CREATE (acc: Account {id: row.id, name: row.name, email: row.email})-[r:LOGGED_ON]->(dev: Device {id: row.device_id})
```

```cypher
LOAD CSV WITH HEADERS FROM 'file:///transactions.csv' AS row FIELDTERMINATOR ','
MATCH (source: Account {id: row.source_account_id}),(target: Account {id: row.target_account_id})
CREATE (source)-[r: SENT_TO {id: row.id, amount: toFloat(row.amount), timestamp: datetime(replace(row.timestamp, " ", "T"))}]->(target)
```

## TODO

 - Wykrywanie transakcji w pętlach (np. A -> B -> C -> A)
 - Kilka kont, jedno urządzenie
 - Communities detection (wąska grupa robiąca transakcje jedynie ze sobą)
 - Maybe location based detection
