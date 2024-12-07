# Fraud Detection Graph

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
