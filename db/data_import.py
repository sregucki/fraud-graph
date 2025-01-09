from neo4j import GraphDatabase

URI = "bolt://localhost:7687"


def main():
    clear_db()
    import_query()


def clear_db():
    driver = GraphDatabase.driver(URI, auth=None)
    query = """
    MATCH (n) DETACH DELETE n
    """
    run_query(driver, query)


def import_query():
    driver = GraphDatabase.driver(URI, auth=None)
    create_devices = """
    LOAD CSV WITH HEADERS FROM 'file:///devices.csv' AS row FIELDTERMINATOR ','
    MERGE (dev: Device {id: row.id, name: row.name})
    """
    create_accounts = """
    LOAD CSV WITH HEADERS FROM 'file:///accounts.csv' AS row FIELDTERMINATOR ','
    MERGE (acc: Account {id: row.id, name: row.name, email: row.email, country: row.country, city: row.city, street_address: row.street_address})
    """

    assign_devices = """
    LOAD CSV WITH HEADERS FROM 'file:///accounts.csv' AS row FIELDTERMINATOR ','
    MATCH (acc: Account {id: row.id})
    MATCH (dev: Device {id: row.device_id})
    MERGE (acc)-[:LOGGED_ON]->(dev)
    """
    create_transactions = """
    LOAD CSV WITH HEADERS FROM 'file:///transactions.csv' AS row FIELDTERMINATOR ','
    MATCH (source: Account {id: row.source_account_id})
    MATCH (target: Account {id: row.target_account_id})
    MERGE (source)-[r: SENT_TO {id: row.id, amount: toFloat(row.amount), timestamp: datetime(replace(row.timestamp, " ", "T"))}]->(target)
    """

    run_query(driver, create_devices)
    run_query(driver, create_accounts)
    run_query(driver, assign_devices)
    run_query(driver, create_transactions)


def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()


if __name__ == "__main__":
    main()
