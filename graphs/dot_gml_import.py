#!/usr/bin/env python3

# This script is for importing recipe graphs written in DOT format into yEd.
# General process: Ask AI for recipe system ideas, and ask it to give you its suggestions as a recipe graph in DOT format. Then run this script, paste in DOT text. Then open GML file in yEd, and use auto-layout to make it readable.
# Code written by Gemini 2.5 Pro.

# The script asks you to paste a graph in DOT format.
# The DOT graph is converted to GML by running `gv2gml`. Both DOT and GML files are saved in /tmp.
# The GML graph is then fixed up a bit (ensuring all nodes have labels, making all labels lowercase) then saved in /tmp.
# Then the GML file can be imported into yEd.
# You need to install gv2gml before running.

import sys
import os
import datetime
import subprocess
import re
import shutil

# --- Configuration ---
TMP_DIR = "/tmp"
DEBUG = True  # Set to True to enable debug printing, False to disable

# --- Helper Functions ---
def check_gv2gml():
    """Checks if gv2gml executable is available in PATH."""
    if shutil.which("gv2gml") is None:
        print("Error: 'gv2gml' command not found.", file=sys.stderr)
        print("Please ensure Graphviz is installed and 'gv2gml' is in your system's PATH.", file=sys.stderr)
        sys.exit(1)

def generate_filenames():
    """Generates unique base filename and full paths for DOT and GML files."""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    base_filename = f"graph-{timestamp}"
    dot_filepath = os.path.join(TMP_DIR, f"{base_filename}.dot")
    gml_filepath = os.path.join(TMP_DIR, f"{base_filename}.gml")
    return dot_filepath, gml_filepath

# Helper function to process the buffered lines for a single node
def process_node_buffer(node_buffer, debug):
    """
    Processes a list of lines representing a single node block.
    Adds/updates labels and sets shape to rectangle.

    Args:
        node_buffer (list): List of strings, lines of the node block.
        debug (bool): Flag to enable debug printing.

    Returns:
        list: List of strings, the modified lines for the node block.
    """
    if not node_buffer:
        return []
    if debug:
        print("-" * 20)
        print(f"DEBUG: Processing Node Buffer (length {len(node_buffer)}):")
        #for i, line in enumerate(node_buffer): print(f"  [{i}] {line}")


    processed_lines = []
    node_name = None
    original_label_line_index = -1
    label_value = None  # Store original label value if found
    has_graphics_block = False
    graphics_start_index = -1
    graphics_end_index = -1
    original_type_line_index = -1
    type_found_in_graphics = False
    name_line_index = -1 # Index where name was found

    # --- Regex Patterns ---
    node_name_pattern = re.compile(r'^\s*name\s+"([^"]+)"')
    label_pattern = re.compile(r'^\s*label\s+"([^"]*)"')
    graphics_start_pattern = re.compile(r'^\s*graphics\s+\[')
    type_pattern = re.compile(r'^\s*type\s+"([^"]+)"')
    # Match graphics end ']' (assumes indent 4 or more)
    graphics_end_pattern = re.compile(r'^\s{4,}\]')
    # Match node end ']' (assumes indent 2)
    node_end_pattern = re.compile(r'^\s{2}\]')


    # --- Pass 1: Find key elements and indices in the buffer ---
    in_graphics = False
    for i, line in enumerate(node_buffer):
        # Find Node Name
        name_match = node_name_pattern.match(line)
        if name_match:
            node_name = name_match.group(1)
            name_line_index = i
            if debug: print(f"  DEBUG: Found name: '{node_name}' at index {i}")

        # Find Existing Label
        label_match = label_pattern.match(line)
        if label_match:
            original_label_line_index = i
            label_value = label_match.group(1)
            if debug: print(f"  DEBUG: Found existing label: '{label_value}' at index {i}")

        # Find Graphics Block Start
        if graphics_start_pattern.match(line):
            has_graphics_block = True
            in_graphics = True
            graphics_start_index = i
            if debug: print(f"  DEBUG: Found graphics start at index {i}")
            continue # Move to next line after finding graphics start

        # Inside Graphics Block
        if in_graphics:
            # Find Existing Type
            if type_pattern.match(line):
                original_type_line_index = i
                type_found_in_graphics = True
                if debug: print(f"  DEBUG: Found existing type at index {i}")

            # Find Graphics Block End
            # Use indent check as primary, fallback to simple ']' if needed
            if line.strip() == ']' and line.startswith('    '): # Typical GML graphics indent
                in_graphics = False
                graphics_end_index = i
                if debug: print(f"  DEBUG: Found graphics end at index {i}")


    # --- Determine Target Label ---
    target_label = ""
    if label_value is not None:  # Use existing label if found
        target_label = label_value.lower()
        if debug: print(f"  DEBUG: Using existing label, lowercased: '{target_label}'")
    elif node_name:  # Otherwise use node name
        target_label = node_name.lower()
        if debug: print(f"  DEBUG: Using node name '{node_name}', lowercased: '{target_label}'")
    else:
         if debug: print(f"  DEBUG: WARNING - No node name found in buffer, cannot generate label.")


    # --- Prepare New/Replacement Lines ---
    # Indentation matters for generated lines
    label_indent = "  " # Typical label indent
    graphics_indent = "  " # Typical graphics block indent
    type_indent = "    " # Typical type indent within graphics

    new_label_line = f'{label_indent}label "{target_label}"' if target_label else None
    new_type_line = f'{type_indent}type "rectangle"'
    new_graphics_start_line = f'{graphics_indent}graphics ['
    new_graphics_end_line = f'{graphics_indent}]'

    label_handled = False
    type_handled = False

    # --- Pass 2: Construct the new node block ---
    # Create a copy to modify, or build a new list
    temp_processed_lines = []
    inserted_graphics_indices = None # Track where new graphics block is inserted

    for i, line in enumerate(node_buffer):

        # 1. Handle Label Replacement
        if i == original_label_line_index:
            if new_label_line:
                temp_processed_lines.append(new_label_line)
                label_handled = True
                if debug: print(f"  DEBUG: Replaced line {i} with new label line.")
            else:
                 if debug: print(f"  DEBUG: Skipped replacing label at line {i} as no target label generated.")
            continue # Skip adding the original label line

        # 2. Handle Type Replacement (within existing graphics block)
        if i == original_type_line_index:
            temp_processed_lines.append(new_type_line)
            type_handled = True
            if debug: print(f"  DEBUG: Replaced line {i} with new type line.")
            continue # Skip adding the original type line

        # 3. Add the original line if not replaced
        temp_processed_lines.append(line)

        # --- Insertions (happen *after* adding the current line) ---

        # 4. Insert New Label (if none existed) - Insert after name line
        if i == name_line_index and not label_handled and original_label_line_index == -1:
            if new_label_line:
                temp_processed_lines.append(new_label_line)
                label_handled = True
                if debug: print(f"  DEBUG: Inserted new label line after name line (index {i}).")

        # 5. Insert New Type (if graphics existed but type didn't) - Insert before graphics end ']'
        if i == graphics_end_index and not type_handled and not type_found_in_graphics:
             # Insert *before* the line just added (which is the graphics ']')
            temp_processed_lines.insert(-1, new_type_line)
            type_handled = True
            if debug: print(f"  DEBUG: Inserted new type line before graphics end ']' at index {i}.")

    # --- Post-Iteration Modifications ---

    # 6. Insert Missing Graphics Block (if none existed)
    #    Find insertion point (after name/label, before node ']')
    if not has_graphics_block:
        insert_point = -1
        # Try inserting after the (potentially new) label line
        for idx, l in enumerate(temp_processed_lines):
             if label_pattern.match(l):
                 insert_point = idx + 1
                 break
        # Fallback: insert after name line
        if insert_point == -1:
            for idx, l in enumerate(temp_processed_lines):
                if node_name_pattern.match(l):
                    insert_point = idx + 1
                    break
        # Fallback: insert before the node's closing ']'
        if insert_point == -1:
             for idx, l in reversed(list(enumerate(temp_processed_lines))):
                 if node_end_pattern.match(l): # Match node end ']'
                     insert_point = idx
                     break

        if insert_point != -1:
            graphics_lines_to_insert = [
                new_graphics_start_line,
                new_type_line,
                new_graphics_end_line
            ]
            temp_processed_lines[insert_point:insert_point] = graphics_lines_to_insert
            if debug: print(f"  DEBUG: Inserted new graphics block at index {insert_point}.")
            type_handled = True # Type was added as part of the new block
        else:
             if debug: print(f"  DEBUG: WARNING - Could not find suitable insertion point for missing graphics block.")


    # 7. Final Fallback for Label Insertion (if still not handled, e.g., no name found)
    #    Insert before the node's closing ']'
    if not label_handled and new_label_line:
        insert_point = -1
        for idx, l in reversed(list(enumerate(temp_processed_lines))):
            if node_end_pattern.match(l): # Match node end ']'
                insert_point = idx
                break
        if insert_point != -1:
             temp_processed_lines.insert(insert_point, new_label_line)
             label_handled = True
             if debug: print(f"  DEBUG: Inserted label line before node end ']' (fallback).")
        else:
             if debug: print(f"  DEBUG: WARNING - Could not find node end ']' to insert fallback label.")


    processed_lines = temp_processed_lines
    if debug: print(f"DEBUG: Finished processing node buffer. Output lines: {len(processed_lines)}")
    if debug: print("-" * 20)
    return processed_lines


def modify_gml_content(gml_content, debug=False):
    """
    Modifies GML content using a buffering approach for node blocks.

    Args:
        gml_content (str): The original GML content as a single string.
        debug (bool): Flag to enable debug printing.

    Returns:
        str: The modified GML content as a single string.
    """
    if debug: print("DEBUG: Starting GML modification process.")
    lines = gml_content.splitlines()
    new_lines = []
    node_buffer = []
    in_node = False
    node_start_pattern = re.compile(r'^\s*node\s+\[') # Allow flexible indent for start
    node_end_pattern = re.compile(r'^\s{2}\]') # Expect node end ']' at indent 2

    for i, line in enumerate(lines):
        # Detect node start
        if node_start_pattern.match(line):
            # If already in a node, process the previous buffer first (error recovery)
            if in_node and node_buffer:
                if debug: print(f"DEBUG: WARNING - Line {i+1}: New 'node [' found before previous one closed? Processing previous buffer.")
                processed_node = process_node_buffer(node_buffer, debug)
                new_lines.extend(processed_node)

            # Start new node buffer
            in_node = True
            node_buffer = [line]
            if debug: print(f"DEBUG: Line {i+1}: Found 'node [', starting buffer.")

        # Inside a node block
        elif in_node:
            node_buffer.append(line)
            # Detect node end (check indentation carefully)
            if node_end_pattern.match(line): # Check if it's the node's closing bracket
                if debug: print(f"DEBUG: Line {i+1}: Found potential node closing ']', processing buffer.")
                processed_node = process_node_buffer(node_buffer, debug)
                new_lines.extend(processed_node)
                in_node = False
                node_buffer = [] # Clear buffer
            # else: continue buffering lines within the node

        # Outside a node block
        else:
            new_lines.append(line)

    # If loop finishes while still in_node (e.g., file ends before node ']')
    if in_node and node_buffer:
         if debug: print("DEBUG: WARNING - End of file reached while still in node block. Processing final buffer.")
         processed_node = process_node_buffer(node_buffer, debug)
         new_lines.extend(processed_node)

    if debug: print("DEBUG: Finished GML modification process.")
    return "\n".join(new_lines)


# --- Main Execution ---
if __name__ == "__main__":
    check_gv2gml()

    print("Paste your DOT file content below. Press Ctrl+D when finished.", file=sys.stderr)
    dot_content = "" # Initialize
    try:
        dot_content = sys.stdin.read()
        if dot_content: # Check if any content was read before EOF
             print("\nEOF detected. Processing input.", file=sys.stderr)
        else:
             print("\nEOF detected, but no input received.", file=sys.stderr)

    except EOFError:
        # This might not be strictly necessary with sys.stdin.read()
        print("\nEOF signal received.", file=sys.stderr)
    except Exception as e:
        print(f"\nError reading stdin: {e}", file=sys.stderr)
        sys.exit(1)

    if not dot_content:
        print("Error: No input content provided.", file=sys.stderr)
        sys.exit(1)

    dot_filepath, gml_filepath = generate_filenames()

    # 1. Save DOT file
    try:
        with open(dot_filepath, 'w') as f:
            f.write(dot_content)
        print(f"DOT content saved to: {dot_filepath}", file=sys.stderr)
    except IOError as e:
        print(f"Error writing DOT file {dot_filepath}: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Run gv2gml
    print(f"Running gv2gml to convert to: {gml_filepath}", file=sys.stderr)
    command = ["gv2gml", dot_filepath, "-o", gml_filepath]
    try:
        # Use shell=False (default and safer)
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
        if DEBUG and result.stdout:
             print(f"DEBUG gv2gml stdout:\n{result.stdout}", file=sys.stderr)
        if result.stderr:
             # Always print stderr from gv2gml as it might contain warnings
             print(f"gv2gml stderr:\n{result.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: 'gv2gml' command not found during execution.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running gv2gml:", file=sys.stderr)
        print(f"Command: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        # Decode stderr/stdout if they are bytes
        stderr_str = e.stderr.decode('utf-8', errors='ignore') if isinstance(e.stderr, bytes) else e.stderr
        stdout_str = e.stdout.decode('utf-8', errors='ignore') if isinstance(e.stdout, bytes) else e.stdout
        print(f"Stderr:\n{stderr_str}", file=sys.stderr)
        print(f"Stdout:\n{stdout_str}", file=sys.stderr)
        try:
            os.remove(dot_filepath)
            print(f"Removed intermediate file: {dot_filepath}", file=sys.stderr)
        except OSError: pass
        sys.exit(1)
    except Exception as e:
         print(f"An unexpected error occurred running gv2gml: {e}", file=sys.stderr)
         sys.exit(1)


    # 3. Read and Modify GML file
    print(f"Modifying GML file: {gml_filepath}", file=sys.stderr)
    try:
        # Specify encoding, often UTF-8
        with open(gml_filepath, 'r', encoding='utf-8') as f:
            original_gml_content = f.read()

        modified_gml_content = modify_gml_content(original_gml_content, debug=DEBUG)

        # Write modified content back, ensure newline at end
        with open(gml_filepath, 'w', encoding='utf-8') as f:
            f.write(modified_gml_content)
            if not modified_gml_content.endswith('\n'):
                 f.write('\n') # Ensure final newline

    except FileNotFoundError:
         print(f"Error: GML file {gml_filepath} not found after conversion.", file=sys.stderr)
         sys.exit(1)
    except IOError as e:
        print(f"Error reading or writing GML file {gml_filepath}: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
         print(f"An unexpected error occurred during GML modification: {e}", file=sys.stderr)
         import traceback
         traceback.print_exc(file=sys.stderr) # Print traceback for easier debugging
         print(f"Original GML saved at: {gml_filepath}", file=sys.stderr)
         sys.exit(1)

    # 4. Success message with final file path
    print(f"\nSuccessfully processed graph.", file=sys.stderr)
    print(f"Final modified GML file is located at:")
    print(gml_filepath) # Print the final path to stdout

    # Optional: Clean up the original .dot file
    # try:
    #     os.remove(dot_filepath)
    #     print(f"Cleaned up intermediate file: {dot_filepath}", file=sys.stderr)
    # except OSError as e:
    #     print(f"Warning: Could not remove intermediate DOT file {dot_filepath}: {e}", file=sys.stderr)
