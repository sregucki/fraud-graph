from neo4j import GraphDatabase


URI = "bolt://localhost:7687"


def main():
    print(multiple_accounts_one_device())


def multiple_accounts_one_device():
    driver = GraphDatabase.driver(URI, auth=None)
    query = """
    MATCH (:Account)-[r:LOGGED_ON]->(d:Device)
    WITH d, count(r) as rel_count
    WHERE rel_count > 1
    RETURN d;
    """
    result = run_query(driver, query)
    return result


def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()


if __name__ == "__main__":
    main()
