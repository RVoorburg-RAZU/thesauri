import os
from rdflib import Graph

def convert_ttl_to_jsonld():
    # Gebruik de huidige directory als invoer- en uitvoermap
    current_directory = os.getcwd()

    # Loop door alle bestanden in de huidige directory
    for filename in os.listdir(current_directory):
        if filename.endswith('.ttl'):
            # Volledige padnamen voor invoer en uitvoer
            input_path = os.path.join(current_directory, filename)
            output_path = os.path.join(current_directory, filename.replace('.ttl', '.json'))

            # Lees het Turtle bestand
            g = Graph()
            g.parse(input_path, format='ttl')

            # Schrijf naar JSON-LD
            g.serialize(destination=output_path, format='json-ld')
            print(f'Converted {input_path} to {output_path}')

# Voer de conversie uit
convert_ttl_to_jsonld()