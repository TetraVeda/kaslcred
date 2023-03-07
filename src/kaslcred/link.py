# -*- coding: utf-8 -*-
"""
KASL KERI and
"""
import json
from collections import namedtuple

from keri.core import scheming, coring

ACDCSchema = namedtuple('ACDCSchema', 'schemaName schemaFilePath dependencies edgeName')


def calc_eval_order(schemas: list[ACDCSchema], evaluation_order=[], popped=[]):
    """
    Calculate the order to evaluate schemas based on the dependency graph.

    Recursive depending on whether any schemas need to be popped to the end
    of the list.
    :param schemas (list[ACDCSchema]):
             The schemas to calculate an evaluation order for.
    :param evaluation_order (list[str]): The ordered array accumulating
             string names of schemas to evaluate. This is the order schemas
             will be processed in.
    : param popped (list[ACDCSchema]): Any schemas that need to be sorted
             further towards the end of the order.
    :return: evaluation_order - the ordered list of schemas to evaluate
    """
    # evaluation_order is a list of schema names
    if len(schemas) == 1:
        return [schemas[0].schemaName]
    if len(popped) > 0:
        schemas.extend(popped)
        popped = []
    popped_index = -1
    for idx, schema in enumerate(schemas):
        pop_schema = False
        for dependency in schema.dependencies:
            # move schema to end of list if any dependencies are missing
            if dependency not in evaluation_order:
                schema = schemas[idx]
                popped_index = idx
                popped.append(schema)
                pop_schema = True
                break
        if pop_schema:
            break
        try:
            evaluation_order.index(schema.schemaName)
            continue  # skip item if already present - eliminates duplicates
        except ValueError:  # if it doesn't exist in the array then add it
            pass

        if schema.dependencies == []:
            evaluation_order.append(schema.schemaName)
        else:
            max_index = len(evaluation_order) - 1
            for dependency in schema.dependencies:
                # already know dependencies are in evaluation_order due to prior check
                dep_index = evaluation_order.index(dependency)  # index of the schema name
                if dep_index > max_index:
                    max_index = dep_index
            if max_index == len(evaluation_order) or max_index + 1 == len(evaluation_order):
                evaluation_order.append(schema.schemaName)
            elif max_index == 0:
                evaluation_order.append(schema.schemaName)
            else:
                evaluation_order.insert(max_index + 1, schema.schemaName)

    if len(popped) > 0:
        if popped_index != -1:
            schemas.remove(schemas[popped_index])
        return calc_eval_order(schemas, evaluation_order, popped)
    popped.clear()
    schemas.clear()
    new_order=[]
    for ord in evaluation_order:
        new_order.append(ord)

    return new_order


def link_schemas(schema_source_root, schemas: list[ACDCSchema]):
    """
    Generate SAIDified schema files based on the schema definitions. Can pretty print the resulting JSON schema files.
    :param schema_source_root (str): The directory in which to look for all of the schema files
    :param schema_results_dir (str): The output directory to write the SAIDified schema files
    :param schemas (list): The list of schemas read in from the schema map
    :param pretty (bool): Whether to pretty print the output JSON. False recommended. Only use True for debugging.
    :return:
    """
    evaluation_order = calc_eval_order(schemas, evaluation_order=[], popped=[])
    schema_results = {}
    saidified_schemas = []
    for schema_name in evaluation_order:
        schema = list(filter(lambda s: s.schemaName == schema_name, schemas))[0]
        saidified = construct_schema(schema, f'{schema_source_root}', schema_results)
        schema_results[schema_name] = (get_schema_said(saidified), schema.edgeName)
        saidified_schemas.append((schema_name, saidified))
    return saidified_schemas


def save_schemas(saidified_schemas: list, schema_results_dir, pretty: bool):
    """Save SAIDified schema to results directory."""
    for (schema_name, schema) in saidified_schemas:
        save_result(schema_name, schema_results_dir, schema, pretty)


def get_schema_said(schema):
    """Get SAID for target schema using default ID symbol."""
    if not schema[coring.Ids.dollar] or schema[coring.Ids.dollar] == "":
        raise RuntimeError(
            f'Cannot get schema SAID: {coring.Ids.dollar} attribute empty or missing from schema {schema}')
    return schema[coring.Ids.dollar]


def construct_schema(schema: ACDCSchema, schema_root_path: str, schema_results: dict):
    """
    Create a linked schema in root_path with needed edges from schema_results.

    Will use any edge name overrides specified in the map file.
    :param schema: schema to construct. Must be a valid file
    :param schema_root_path: Location to read the schema files from
    :param schema_results: dict of schemaName : (SAID, edgeName) entries
    """
    for dep in schema.dependencies:
        if dep not in schema_results:
            raise RuntimeError(f'Schema {schema.schemaName} depends on schema {key} and it was not in results dict.')
    edges = {key: schema_results[key] for key in schema.dependencies}
    schema_source = __load(f'{schema_root_path}/{schema.schemaFilePath}')
    for edge, (said, edgeName) in edges.items():
        edge_name = edgeName if edgeName != '' and edgeName is not None else edge
        schema_source = update_schema_edge(edge_name,
                                           schema_source, said)
    return populateSAIDS(schema_source)


def update_schema_edge(edge_name, target_schema, far_said):
    """
    Add the far_said into the target_schema on the specified edge_name.

    :param edge_name: The edge of the target_schema to find and update.
    :param target_schema: The target schema to update with the far_said SAID
    :param far_said: Schema SAID of the far side ACDC node.
    :return: The updated JSON for the target_schema
    """
    edge_idx = find_edge_index(edge_name, target_schema)
    target_schema['properties']['e']['oneOf'][edge_idx]['properties'][edge_name]['properties']['s']['const'] = far_said
    return target_schema


def find_edge_index(edge_name, target_schema):
    """
    Find the edge index of the specified edge name for the target schema or raise an exception.

    :param edge_name: Name of the edge to find.
    :param target_schema: Schema to look for the edge in.
    :return: index of the specified edge name in the target schema.
    """
    if not (credential_type := target_schema['credentialType']):
        raise RuntimeError(f'Malformed schema, missing credentialType attribute. Schema: {target_schema}')
    edge_idx = None
    if schema := target_schema['properties']:
        if edges := schema['e']:
            if oneOf := edges['oneOf']:
                for idx, edge in enumerate(oneOf):
                    try:
                        props = edge['properties']
                        if props[edge_name]:
                            edge_idx = idx
                    except KeyError:
                        continue
                if edge_idx is None:
                    raise RuntimeError(f'Edge {edge_name} expected yet not found in target schema {credential_type}')
    return edge_idx


def __load(p):
    ff = open(p, 'r')
    jsn = json.load(ff)
    ff.close()
    return jsn


def save_result(name, path, schema, pretty_print=True):
    """Save linked schema to specified result directory."""
    schemer = scheming.Schemer(sed=schema)
    with open(f'{path}/{name}__{schemer.said}.json', "wb") as schema_file:
        # schema_file.write(schemer.raw)
        if pretty_print:
            jsn = json.loads(bytes(schemer.raw))
            schema_file.write(json.dumps(jsn, indent=2).encode())
        else:
            schema_file.write(schemer.raw)


def read_schema_map(schema_map_file_path: str) -> list[ACDCSchema]:
    """Read schema map file."""
    with open(schema_map_file_path, 'r') as file:
        data = json.load(file)
        return [ACDCSchema(**k) for k in data["schemas"]]


def populateSAIDS(schema: dict, idage: str = coring.Ids.dollar,
                  code: str = coring.MtrDex.Blake3_256):
    """
    Calculate and write self addressing identifiers (SAIDS).

    Applies to root, attribute (a), edge (e), and rules (r) sections.
    :param schema (dict): The schema to calculate SAIDs for and write to
    :param idage (str): The property name to use to write SAIDs to.
                        Defaults to "$id"
    :param code (str): The type of digest function to us to create SAIDs.
    :return: The schema dict updated with SAIDs
    """
    if 'properties' in schema:
        props = schema['properties']

        # check for top level ids
        for v in ["a", "e", "r"]:
            if v in props and '$id' in props[v]:
                vals = props[v]
                vals[idage] = coring.Saider(sad=vals, code=code, label=idage).qb64
            elif v in props and 'oneOf' in props[v]:
                if isinstance(props[v]['oneOf'], list):
                    # check each 'oneOf' for an id
                    ones = props[v]['oneOf']
                    for o in ones:
                        if isinstance(o, dict) and idage in o:
                            o[idage] = coring.Saider(sad=o, code=code, label=idage).qb64

    schema[idage] = coring.Saider(sad=schema, code=code, label=idage).qb64

    return schema


def main(schema_source, schema_results, schema_map, prettyprint):
    """Run the schema linker."""
    schemas = read_schema_map(schema_map)
    saidified_schemas = link_schemas(schema_source, schemas)
    save_schemas(saidified_schemas, schema_results, prettyprint)


if __name__ == "__main__":
    import sys

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
