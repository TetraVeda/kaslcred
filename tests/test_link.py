from src.kaslcred.link import ACDCSchema, calc_eval_order, read_schema_map, link_schemas


def test_calc_eval_order():
    test_schemas = [
        ACDCSchema("helloAttend", "hello-attend-schema.json", ["helloAdmit"], ""),
        ACDCSchema("helloAdmit", "hello-admit-schema.json", ["helloKERI", "helloACDC"], ""),
        ACDCSchema("helloKERI", "hello-keri-schema.json", [], ""),
        ACDCSchema("helloACDC", "hello-acdc-schema.json", ["helloKERI"], "")
    ]
    order = calc_eval_order(test_schemas)
    assert order == ["helloKERI", "helloACDC", "helloAdmit", "helloAttend"]


def test_link_schemas():
    print("test works")
    schema_map = read_schema_map("./sample_schemas/single-schema-map.json")
    results = link_schemas("./sample_schemas", schema_map)
    assert len(results) == 1
    (_name, saidified) = results[0]
    assert saidified['$id'] == "EAlUDQH6-DS3Fc2gTKQdwKz9jlI2yDfBRr5cuZLbCwvN"
    # TODO asset
