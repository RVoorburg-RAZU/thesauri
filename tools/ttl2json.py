import os
from rdflib import Graph

def convert_ttl_to_jsonld():
    # Use the 'rdf' directory relative to this script as input, and write outputs to root-level 'generated'
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_directory = os.path.abspath(os.path.join(script_dir, '..', 'rdf'))
    # Ensure a root-level 'generated' directory exists for output
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    output_directory = os.path.join(project_root, 'generated')
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over all files in the rdf directory
    for filename in os.listdir(target_directory):
        if filename.endswith('.ttl'):
            # Full paths for input and output
            input_path = os.path.join(target_directory, filename)
            output_path = os.path.join(output_directory, filename.replace('.ttl', '.json'))

            # Read the Turtle file
            g = Graph()
            g.parse(input_path, format='ttl')

            # Write to JSON-LD
            g.serialize(destination=output_path, format='json-ld')
            print(f'Converted {input_path} to {output_path}')

# Run the conversion
convert_ttl_to_jsonld()