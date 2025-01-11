from neo4j import GraphDatabase

URI = "bolt://localhost:7687"

def main():
    driver = GraphDatabase.driver(URI, auth=None)
    
    print(multiple_accounts_one_device())
    print(community_detection(driver))

def community_detection(driver):
    # print("Creating Graph Projection.")
    # create_graph_projection(driver)
    print("Detecting Communities.")
    community_stats = detect_communities(driver)
    print("Community Stats:", community_stats)
    community_details = get_community_results(driver)
    formatted_details = format_community_results(community_details)
    print(formatted_details)

def create_graph_projection(driver):
    query = """
    CALL gds.graph.project(
        'fraudGraph',
        ['Account'],
        {
            SENT_TO: {
                type: 'SENT_TO',
                orientation: 'UNDIRECTED'
            }
        }
    )
    """
    run_query(driver, query)

def detect_communities(driver):
    query = """
    CALL gds.louvain.write(
        'fraudGraph',
        {
            writeProperty: 'community'
        }
    )
    YIELD communityCount, modularity;
    """
    return run_query(driver, query)


def get_community_results(driver):
    query = """
    MATCH (a:Account)
    RETURN a.community AS community, collect(a.name) AS accounts
    ORDER BY size(accounts) DESC;
    """
    return run_query(driver, query)

def format_community_results(community_results):
    formatted = []
    for record in community_results:
        community = record.get('community')
        accounts = record.get('accounts', [])
        formatted.append(f"Community {community}:\n  Accounts: " + ", ".join(accounts))
    return "\n\n".join(formatted)


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
