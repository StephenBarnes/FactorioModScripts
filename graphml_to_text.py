#!/usr/bin/env python3

# This file converts .graphml files from yEd representing sets of recipes into a text format.
# It assumes the yEd file has nodes that are #FFCC99 representing recipes, and nodes #CCFFFF for items/fluids.
# The yEd file should have an arrow from every item/fluid to recipes where it's an ingredient, and an arrow from every recipe to items/fluids it produces.
# The resulting text format has one line for every recipe, like: `recipe_name: input1 + input2 -> output1 + output2`.
# Code written by Gemini 2.5 Pro.

import xml.etree.ElementTree as ET
import sys
import argparse
from collections import defaultdict

# Define the yEd/GraphML namespaces to correctly parse the file
# Using a placeholder for the default namespace is common practice
NAMESPACES = {
    'gm': 'http://graphml.graphdrawing.org/xmlns',
    'y': 'http://www.yworks.com/xml/graphml',
    'yed': 'http://www.yworks.com/xml/yed/3',
    # Add other namespaces if your yEd file uses them
}

# Define the colors used to identify node types
ITEM_COLOR = "#CCFFFF"
RECIPE_COLOR = "#FFCC99"

def get_node_info(node_element):
    """Extracts ID, label, and type (item, recipe, or unknown) from a node element."""
    node_id = node_element.get('id')
    if not node_id:
        return None, None, None

    label = None
    node_label_element = node_element.find('.//y:NodeLabel', NAMESPACES)
    if node_label_element is not None and node_label_element.text:
        label = node_label_element.text.strip()
        label = label.replace("\n", " ")

    color = None
    fill_element = node_element.find('.//y:Fill', NAMESPACES)
    if fill_element is not None:
        color = fill_element.get('color')

    node_type = 'unknown'
    if color:
        if color.upper() == ITEM_COLOR.upper():
            node_type = 'item'
        elif color.upper() == RECIPE_COLOR.upper():
            node_type = 'recipe'

    if not label:
         print(f"Warning: Node '{node_id}' has no label.", file=sys.stderr)
         label = f"UNKNOWN_NODE_{node_id}" # Assign placeholder if label missing


    return node_id, label, node_type

def process_graphml(graphml_file):
    """
    Parses a yEd GraphML file and prints Factorio recipes.

    Args:
        graphml_file (str): Path to the GraphML file.
    """
    try:
        tree = ET.parse(graphml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found: {graphml_file}", file=sys.stderr)
        sys.exit(1)

    graph_element = root.find('gm:graph', NAMESPACES)
    if graph_element is None:
        print("Error: Could not find <graph> element in the GraphML file.", file=sys.stderr)
        sys.exit(1)

    nodes_info = {} # Store {node_id: (label, type)}
    recipe_nodes = {} # Store {recipe_id: {'name': recipe_name, 'inputs': [], 'outputs': []}}

    # --- Pass 1: Process all nodes ---
    for node_element in graph_element.findall('gm:node', NAMESPACES):
        node_id, label, node_type = get_node_info(node_element)
        if node_id:
            nodes_info[node_id] = (label, node_type)
            if node_type == 'recipe':
                recipe_nodes[node_id] = {'name': label, 'inputs': [], 'outputs': []}

    if not recipe_nodes:
        print("No recipe nodes (orange color: {}) found in the graph.".format(RECIPE_COLOR))
        return

    # --- Pass 2: Process all edges to link items and recipes ---
    for edge_element in graph_element.findall('gm:edge', NAMESPACES):
        source_id = edge_element.get('source')
        target_id = edge_element.get('target')

        if not source_id or not target_id:
            print(f"Warning: Skipping edge with missing source/target ID.", file=sys.stderr)
            continue

        # Check if source and target nodes exist in our parsed info
        if source_id not in nodes_info or target_id not in nodes_info:
            print(f"Warning: Skipping edge connecting unknown node(s): {source_id} -> {target_id}", file=sys.stderr)
            continue

        source_label, source_type = nodes_info[source_id]
        target_label, target_type = nodes_info[target_id]

        # Edge: Item -> Recipe (Input)
        if source_type == 'item' and target_type == 'recipe':
            if target_id in recipe_nodes:
                recipe_nodes[target_id]['inputs'].append(source_label)
            else:
                 print(f"Warning: Edge points to recipe node '{target_id}' ({target_label}) which was not correctly identified.", file=sys.stderr)


        # Edge: Recipe -> Item (Output)
        elif source_type == 'recipe' and target_type == 'item':
            if source_id in recipe_nodes:
                recipe_nodes[source_id]['outputs'].append(target_label)
            else:
                print(f"Warning: Edge originates from recipe node '{source_id}' ({source_label}) which was not correctly identified.", file=sys.stderr)


    # --- Pass 3: Format and print the recipes ---
    #print("--- Factorio Recipes ---")
    for recipe_id, data in recipe_nodes.items():
        recipe_name = data['name']
        # Sort inputs and outputs alphabetically for consistent output
        inputs_str = " + ".join(sorted(data['inputs'])) if data['inputs'] else " " # Use space if no inputs? Or empty string? Let's use empty for clarity.
        outputs_str = " + ".join(sorted(data['outputs'])) if data['outputs'] else ""

        # Handle cases where inputs or outputs might be missing entirely
        if not inputs_str.strip(): inputs_str = "<none>"
        if not outputs_str.strip(): outputs_str = "<none>"


        print(f"{recipe_name}: {inputs_str} -> {outputs_str}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert yEd GraphML Factorio recipes to text format.')
    parser.add_argument('graphml_file', help='Path to the yEd GraphML file.')
    args = parser.parse_args()

    process_graphml(args.graphml_file)
