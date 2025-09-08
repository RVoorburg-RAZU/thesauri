# RAZU thesauri

Thesauri in RDF for the RAZU e-depot / digital repository.

## How to use

1. Use the turtle files in the `rdf` directory for updating the concepts.

2. Run `python tools/validate.py` to validate the RDF against a SHACL profile.

3. Run `python tools/ttl2json.py` to convert the turtle files to json (the prefered format for the repository)

4. Upload the json-files to the `context` bucket (tool = TODO)

5. Upload the files to the relevant datasets in the triplestore (documentation = TODO, automation = TODO).
Each thesaurus has its own dataset in the Triply environment. Each thesaurus is also upload to the id/object dataset to allow all data to be queried from a single SPARQL endpoint.

