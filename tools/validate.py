import os
import sys
from rdflib import Graph

try:
    # pyshacl provides SHACL validation for RDF graphs
    from pyshacl import validate as shacl_validate
except ImportError:  # pragma: no cover
    shacl_validate = None


def validate_all_ttl():
    """
    Validate all .ttl files in the project's rdf/ directory against SHACL shapes in shacl/thesauri.ttl.

    - Input directory: ../rdf relative to this script
    - Shapes file: ../shacl/thesauri.ttl
    - Output directory for reports: ../generated/validation

    For each TTL file, writes:
      - <name>_shacl_report.ttl: SHACL report graph
      - <name>_shacl_report.txt: Human-readable validation report
    Exits with code 1 if any file does not conform; 0 otherwise.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    rdf_dir = os.path.join(project_root, 'rdf')
    shapes_path = os.path.join(project_root, 'shacl', 'thesauri.ttl')
    out_dir = os.path.join(project_root, 'generated', 'validation')

    # Ensure output directory exists
    os.makedirs(out_dir, exist_ok=True)

    # Basic checks
    if not os.path.isdir(rdf_dir):
        print(f"ERROR: RDF directory not found: {rdf_dir}", file=sys.stderr)
        sys.exit(2)
    if not os.path.isfile(shapes_path):
        print(f"ERROR: SHACL shapes file not found: {shapes_path}", file=sys.stderr)
        sys.exit(2)
    if shacl_validate is None:
        print(
            "ERROR: pyshacl is not installed. Install it with: pip install pyshacl",
            file=sys.stderr,
        )
        sys.exit(2)

    # Load shapes graph once
    shapes_graph = Graph()
    shapes_graph.parse(shapes_path, format='turtle')

    failures = 0
    checked = 0

    for filename in sorted(os.listdir(rdf_dir)):
        if not filename.endswith('.ttl'):
            continue

        input_path = os.path.join(rdf_dir, filename)
        base_name = os.path.splitext(filename)[0]
        report_ttl_path = os.path.join(out_dir, f"{base_name}_shacl_report.ttl")
        report_txt_path = os.path.join(out_dir, f"{base_name}_shacl_report.txt")

        # Parse data graph
        data_graph = Graph()
        try:
            data_graph.parse(input_path, format='turtle')
        except Exception as e:
            failures += 1
            checked += 1
            msg = f"PARSING ERROR in {input_path}: {e}"
            print(msg)
            with open(report_txt_path, 'w', encoding='utf-8') as f:
                f.write(msg + "\n")
            continue

        # Validate using pyshacl
        try:
            conforms, report_graph, report_text = shacl_validate(
                data_graph,
                shacl_graph=shapes_graph,
                inference='rdfs',  # enable simple RDFS inference
                advanced=True,
                serialize_report_graph=True,
            )
        except Exception as e:
            failures += 1
            checked += 1
            msg = f"VALIDATION ERROR in {input_path}: {e}"
            print(msg)
            with open(report_txt_path, 'w', encoding='utf-8') as f:
                f.write(msg + "\n")
            continue

        # Save reports
        try:
            # report_graph is a serialized string when serialize_report_graph=True
            if isinstance(report_graph, (bytes, str)):
                with open(report_ttl_path, 'wb') as f:
                    f.write(report_graph if isinstance(report_graph, bytes) else report_graph.encode('utf-8'))
            else:
                report_graph.serialize(destination=report_ttl_path, format='turtle')

            with open(report_txt_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
        except Exception as e:
            print(f"WARNING: Failed to write reports for {input_path}: {e}")

        status = "PASS" if conforms else "FAIL"
        print(f"[{status}] {input_path} -> {report_txt_path}")
        checked += 1
        if not conforms:
            failures += 1

    print(f"Checked: {checked}, Failures: {failures}")
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    validate_all_ttl()