"""KASLCred schema linker."""
import sys
from .link import main

if len(sys.argv) < 4:
    raise SystemExit(
        "Usage: python link.py [schema_source_dir] [schema_results_dir] [schema_map] [pretty_print]")
schema_source_dir = sys.argv[1]
schema_results_dir = sys.argv[2]
schema_map_file_path = sys.argv[3]
if len(sys.argv) == 5 and sys.argv[4] == 'true':
    pretty = True
else:
    pretty = False

main(schema_source_dir, schema_results_dir, schema_map_file_path, pretty)
