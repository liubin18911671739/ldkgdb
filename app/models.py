from py2neo import Graph, Node, Relationship
import os

# Retrieve the Neo4j connection information from environment variables
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4j")

# Create a neo4j Graph instance
graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def create_properties_string(properties):
    """Helper function to create properties string for Cypher queries"""
    return ", ".join(f"{k}:{v}" for k, v in properties.items())


def create_node(label, properties):
    node = Node(label, **properties)
    graph.create(node)
    return node.to_dict()


def create_relationship(node1, node2, rel_type, properties=None):
    if not properties:
        properties = {}
    rel = Relationship(node1, rel_type, node2, **properties)
    graph.create(rel)
    return rel.to_dict()


def execute_query(query, params=None):
    if not params:
        params = {}
    result = graph.run(query, params)
    return [record.to_dict() for record in result]


def merge_node(label, properties):
    query_properties = create_properties_string(properties)
    query = f"MERGE (n:{label} {{{query_properties}}}) RETURN n"
    return execute_query(query)


def delete_node(label, properties):
    query_properties = create_properties_string(properties)
    query = f"MATCH (n:{label} {{{query_properties}}}) DETACH DELETE n"
    return execute_query(query)
