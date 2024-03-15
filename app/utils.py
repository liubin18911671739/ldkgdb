from collections import defaultdict

import csv
import json
from rdflib import Graph as RDFGraph

from app.models import (
    create_node,
    create_relationship,
    execute_query,
    merge_node,
    delete_node,
)


def create_nodes_and_relationships(node_label, node_data):
    nodes = []
    relationships = []

    node_properties = node_data.copy()
    node = create_node(node_label, node_properties)
    nodes.append(node)

    for key, value in node_data.items():
        if key.startswith("rel_"):
            rel_type = key[4:]
            related_node_properties = value
            related_node = create_node(node_label, related_node_properties)
            rel_properties = {}
            relationship = create_relationship(
                node, related_node, rel_type, rel_properties
            )
            relationships.append(relationship)

    return nodes, relationships


def import_csv(file):
    nodes = []
    relationships = []
    reader = csv.DictReader(file)
    for row in reader:
        n, r = create_nodes_and_relationships(row.pop("label"), row)
        nodes.extend(n)
        relationships.extend(r)

    return {"nodes": nodes, "relationships": relationships}


def import_json(file):
    data = json.load(file)
    nodes = []
    relationships = []

    for node_data in data.get("nodes", []):
        n, r = create_nodes_and_relationships(node_data.pop("label"), node_data)
        nodes.extend(n)
        relationships.extend(r)

    return {"nodes": nodes, "relationships": relationships}


def import_rdf(file):
    graph = RDFGraph().parse(file)
    nodes = []
    relationships = []

    for subject, predicate, object in graph:
        subject_node = create_node("Resource", {"uri": str(subject)})
        object_node = create_node("Resource", {"uri": str(object)})
        nodes.extend([subject_node, object_node])

        relationship = create_relationship(subject_node, object_node, str(predicate))
        relationships.append(relationship)

    return {"nodes": nodes, "relationships": relationships}


def import_file(file, file_type):
    dispatchers = defaultdict(
        lambda: (lambda x: None),
        {"csv": import_csv, "json": import_json, "rdf": import_rdf},
    )

    if file_type not in dispatchers:
        raise ValueError("Invalid file type")

    return dispatchers[file_type](file)
