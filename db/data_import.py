from neo4j import GraphDatabase

URI = "bolt://localhost:7687"


def main():
    import_query()


def import_query():
    driver = GraphDatabase.driver(URI, auth=None)
    query_accounts = """
    LOAD CSV WITH HEADERS FROM 'file:///accounts.csv' AS row FIELDTERMINATOR ','
    CREATE (acc: Account {id: row.id, name: row.name, email: row.email, country: row.country, city: row.city, street_address: row.street_address})-[r:LOGGED_ON]->(dev: Device {id: row.device_id})
    """
    query_transactions = """
    LOAD CSV WITH HEADERS FROM 'file:///transactions.csv' AS row FIELDTERMINATOR ','
    MATCH (source: Account {id: row.source_account_id}),(target: Account {id: row.target_account_id})
    CREATE (source)-[r: SENT_TO {id: row.id, amount: toFloat(row.amount), timestamp: datetime(replace(row.timestamp, " ", "T"))}]->(target)
    """
    run_query(driver, query_accounts)
    run_query(driver, query_transactions)


def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()


if __name__ == "__main__":
    main()
