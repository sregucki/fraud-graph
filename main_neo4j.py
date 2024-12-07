from neo4j import GraphDatabase


URI = "bolt://localhost:7687"


def main():
    example_query()


def example_query():
    driver = GraphDatabase.driver(URI, auth=("neo4j", "neo4j"))
    query_create = "CREATE (n:Person {name: 'Alice'})"
    query_match = "MATCH (n:Person) RETURN n.name"
    delete_query = "MATCH (n) DETACH DELETE n"
    run_query(driver, query_create)
    result = run_query(driver, query_match)
    run_query(driver, delete_query)
    print(result)


def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return result.data()


if __name__ == "__main__":
    main()
