import ast
import copy
import re
import traceback

import yaml
from docstring_parser import parse

from constants import (
    EXCLUDED_FUNCTIONS,
    EXCLUDED_PARAMS,
    DEFAULT_RESPONSE_TEMPLATE,
    DESCRIPTION,
)


def extract_docstrings(file_path):
    """
    Extract the docstrings of the public functions in a Python file.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        dict: A dictionary where keys are function names and values are docstrings.
    """
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    docstrings = {}

    # Walk through all nodes in the file
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name not in EXCLUDED_FUNCTIONS and not node.name.startswith("_"):
            docstring = ast.get_docstring(node)
            if docstring:
                docstrings[node.name] = docstring

    return docstrings


def map_type(type_name):
    """
    Map a docstring type name to an OpenAPI type.

    Returns:
        tuple: (OpenAPI type, OpenAPI item type for arrays or None)
    """
    type_name = (type_name or "").lower()

    # lists first, then dicts, then scalars: "dict[str, int]" must not be taken for an int
    if "list[int]" in type_name or "list of int" in type_name:
        return "array", "integer"
    if "list[str]" in type_name or "list of str" in type_name:
        return "array", "string"
    if "list[float]" in type_name or "list of float" in type_name:
        return "array", "number"
    if "list[bool]" in type_name or "list of bool" in type_name:
        return "array", "boolean"
    if "list" in type_name:
        return "array", "object"
    if "dict" in type_name:
        return "object", None
    if "int" in type_name:
        return "integer", None
    if "float" in type_name:
        return "number", None
    if "bool" in type_name:
        return "boolean", None
    return "string", None  # Default type (fallback)


def extract_parameters(parsed):
    """
    Extract parameters from a docstring and format them as OpenAPI parameters.
    """
    parameters = []

    # Iterate over the parameters in the docstring
    # print(f"Parameters: {parsed.params}")
    for param in parsed.params:
        # Skip excluded parameters that we don't want to appear in the API documentation
        if param.arg_name in EXCLUDED_PARAMS:
            continue

        # Map each parameter to OpenAPI format
        param_type, item_type = map_type(param.type_name)
        # A dict is passed in the URL as a JSON string, so document it as one
        if param_type == "object":
            param_type = "string"

        print(
            f"Param: {param.arg_name}, Type: {param_type}, Optional: {param.is_optional} {param.description}"
        )
        is_required = not param.is_optional

        schema = {"type": param_type}
        if param_type == "array":
            # repeated query parameter (?id=1&id=2): the OpenAPI 3 default for
            # query arrays (style "form", explode true)
            schema["items"] = {"type": item_type}

        parameter_schema = {
            "name": param.arg_name,
            "in": "query",
            "required": is_required,
            "description": param.description,
            "schema": schema,
        }

        parameters.append(parameter_schema)

    return parameters


def extract_parameters_as_json(parsed):
    """
    Extract parameters from a docstring and format them as JSON schema for OpenAPI.
    """
    properties = {}
    required_parameters = []

    print(f"Parameters(json): {parsed.params}")
    for param in parsed.params:
        # Skip excluded parameters that we don't want to appear in the API documentation
        if param.arg_name in EXCLUDED_PARAMS:
            continue

        # Map the type to OpenAPI type
        param_type, item_type = map_type(param.type_name)

        # Build schema for the parameter
        param_schema = {"type": param_type, "description": param.description}

        if param_type == "array":
            param_schema["items"] = {"type": item_type}  # Default array item type

        properties[param.arg_name] = param_schema

        if not param.is_optional:
            required_parameters.append(param.arg_name)

    return {"type": "object", "properties": properties, "required": required_parameters}


# Boilerplate most docstrings open their Returns section with, e.g.
# "The system response `{...}`." or "dictionary `{'success': True/False, ...}`".
# The envelope it names is already in the response schema, so it's dropped
# from descriptions. A bare "The system response" only counts as boilerplate
# when the sentence ends there ("The system response with ..." is kept).
ENVELOPE_BOILERPLATE_RE = re.compile(
    r"^(?:The system response(?:\s*(`+)\{[^`]*\}\1)?\."
    r"|dictionary\s*(`+)\{[^`]*success[^`]*\}\2\.?)\s*"
)
# Bare type names in a typed shape like {"async_id": str, "request_id": str}
TYPE_NAMES = ("str", "int", "float", "bool", "dict", "list")
BARE_TYPE_RE = re.compile(rf"(?<![\"'\w])({'|'.join(TYPE_NAMES)})(?![\"'\w])")


def find_dict_literal(text):
    """
    Return the first balanced {...} substring of text, or None.
    """
    start = text.find("{")
    if start < 0:
        return None
    depth = 0
    for end in range(start, len(text)):
        depth += {"{": 1, "}": -1}.get(text[end], 0)
        if depth == 0:
            return text[start : end + 1]
    return None


def parse_typed_shape(text):
    """
    Parse the first typed dict literal in a Returns description, e.g.
    '{"success": bool, "message": str, "data": {"async_id": str}}', into an
    OpenAPI schema. Returns None if there is no literal, it isn't parseable
    (e.g. placeholders like <payload data> or {...}), or it is an example with
    values rather than types (e.g. {"success": True, "data": {"key": "value"}}).
    """
    literal = find_dict_literal(text)
    if literal is None:
        return None
    try:
        shape = ast.literal_eval(BARE_TYPE_RE.sub(r'"\1"', literal))
    except (ValueError, SyntaxError):
        return None

    def only_types(value):
        if isinstance(value, dict):
            return all(only_types(v) for v in value.values())
        return value in TYPE_NAMES

    def to_schema(value):
        if isinstance(value, dict):
            return {"type": "object", "properties": {k: to_schema(v) for k, v in value.items()}}
        value_type, item_type = map_type(str(value))
        schema = {"type": value_type}
        if value_type == "array":
            schema["items"] = {"type": item_type}
        return schema

    return to_schema(shape) if isinstance(shape, dict) and only_types(shape) else None


def split_section(docstring, header):
    """
    Split a custom docstring section (e.g. "API details:", "Response data:") out
    of a docstring. The section is its header line plus every following line
    that is blank or indented deeper than the header.

    Returns:
        tuple: (the section's body lines, dedented, or None if absent;
                the docstring with the section removed)
    """
    lines = docstring.splitlines()
    for start, line in enumerate(lines):
        if line.strip() == header:
            indent = len(line) - len(line.lstrip())
            end = start + 1
            while end < len(lines) and (not lines[end].strip() or len(lines[end]) - len(lines[end].lstrip()) > indent):
                end += 1
            body = [body_line.strip() for body_line in lines[start + 1 : end]]
            while body and not body[-1]:
                body.pop()
            return body, "\n".join(lines[:start] + lines[end:])
    return None, docstring


def parse_response_data(docstring):
    """
    Build the schema of the response's "data" field from the "Response data:"
    section, if the docstring has one:

        Response data:
            list[dict]: One entry per requested job ID, in the same order.
                {"status": str, "command": str}
            On failure: {"code": int}, the error code.

    The first line is "<type>: <description>"; the type gives the schema type
    and the rest is the description. A typed shape in the description (before
    any "On failure:") gives the object's fields, or the array items' fields,
    and is then dropped from the description text.

    Returns:
        dict: the "data" schema, or None if there is no "Response data:" section
    """
    body, _ = split_section(docstring, "Response data:")
    if not body:
        return None
    type_name, _, first_line = body[0].partition(":")
    description = " ".join(" ".join([first_line] + body[1:]).split())

    if type_name.strip() == "None":  # nothing in data: no type, just the description
        return {"description": description}
    data_type, item_type = map_type(type_name)
    schema = {"type": data_type, "description": description}
    if data_type == "array":
        # a tuple comes out of the JSON encoder as an array of mixed values
        schema["items"] = {"type": "array", "items": {}} if "tuple" in type_name.lower() else {"type": item_type}

    success_text = description.split("On failure:")[0]
    shape = parse_typed_shape(success_text)
    if shape and data_type in ("array", "object"):
        if data_type == "array":
            schema["items"] = shape
        else:
            schema["properties"] = shape["properties"]
        schema["description"] = " ".join(description.replace(find_dict_literal(success_text), "", 1).split())
    return schema


def build_responses(parsed_docstring, data_schema=None):
    """
    Build the responses for an endpoint, starting from the default template.
    If the docstring has a "Response data:" section, data_schema (from
    parse_response_data) is the "data" field's schema; otherwise it is derived
    from the Returns section. The 200 response keeps the template's short
    description, since Redoc shows it as the response's header; the Returns
    text goes in the body schema instead:
      - str returns: a plain-text body, without the JSON envelope, with the
        Returns text as the string's description.
      - dict returns: the JSON envelope, with the Returns text as the "data"
        field's description, and a typed "data" schema when the docstring
        writes the shape out (e.g. {"data": {"async_id": str}}).
    """
    responses = copy.deepcopy(DEFAULT_RESPONSE_TEMPLATE)
    returns = parsed_docstring.returns
    data = responses["200"]["content"]["application/json"]["schema"]["properties"]["data"]
    if data_schema:  # the "Response data:" section wins over the free-text Returns
        data.clear()
        data.update(data_schema)
        return responses
    if not returns or not returns.description:
        return responses

    description = " ".join(returns.description.split())
    if map_type(returns.type_name)[0] == "string":
        responses["200"]["content"] = {
            "text/plain": {"schema": {"type": "string", "description": description}}
        }
        return responses

    description = ENVELOPE_BOILERPLATE_RE.sub("", description)
    # Only boilerplate, or text about success/message alone ("When unsuccessful, the
    # message field ..."): it says nothing about data, keep the template's generic text
    if "data" not in description.lower():
        return responses
    data["description"] = description
    shape = parse_typed_shape(description)
    if shape and "data" in shape.get("properties", {}):
        data.update(shape["properties"]["data"])
    return responses


def get_custom_metadata(docstring):
    # Parse the docstring manually for the custom section
    doc_lines = docstring.splitlines()
    custom_section_name = "API details:"
    custom_sections = {}
    inside_custom_section = False

    for line in doc_lines:
        stripped_line = line.strip()
        if stripped_line == custom_section_name:
            inside_custom_section = True
            continue  # Skip the section header line
        if inside_custom_section:
            if stripped_line == "" or ":" not in stripped_line:  # End of custom section
                break
            key, value = map(str.strip, stripped_line.split(":", 1))
            custom_sections[key] = value

    return custom_sections


def convert_docstrings_to_openapi(docstrings, tag):
    """
    Convert extracted docstrings to OpenAPI format.

    Args:
        docstrings (dict): A dictionary where keys are function/class/module names and values are docstrings.

    Returns:
        dict: A dictionary where keys are function/class/module names and values are OpenAPI descriptions.
    """

    paths = {}

    for name, docstring in docstrings.items():
        try:
            parsed_docstring = parse(docstring)
            summary = parsed_docstring.short_description

            # Remove the custom sections from the long description
            description = parsed_docstring.long_description or ""
            for section in ("API details:", "Response data:"):
                _, description = split_section(description, section)
            description = description.strip()

            custom_metadata = get_custom_metadata(docstring)
            method = custom_metadata.get("HTTP Method", "POST").lower()
            path = custom_metadata.get("Path", name)
            if "Path" not in custom_metadata:
                print(f"WARNING: {name} has no 'Path:' under 'API details:', documenting it as '{path}'")

            paths[path] = {}
            paths[path][method] = {
                "summary": summary,
                "description": description,
                "tags": [tag],
            }

            # Extract parameters from the docstring
            parameters = extract_parameters(parsed_docstring)
            if method in ["post", "put"]:
                request_body_schema = extract_parameters_as_json(parsed_docstring)
                paths[path][method]["requestBody"] = {
                    "required": True,
                    "content": {"application/json": {"schema": request_body_schema}},
                }
            elif method in ["get", "delete"]:
                paths[path][method]["parameters"] = parameters

            paths[path][method]["responses"] = build_responses(parsed_docstring, parse_response_data(docstring))

        except (AttributeError, TypeError):
            print(
                f"Docstring for {name} could not be parsed. Failed with error:\n{traceback.format_exc()}"
            )

    return paths


if __name__ == "__main__":
    # Define the path to the Python file to convert
    base_path = "panda-server/pandaserver/api/v1/"
    file_paths = [
        "async_process_api.py",
        "credential_management_api.py",
        "data_carousel_api.py",
        "event_api.py",
        "file_server_api.py",
        "harvester_api.py",
        "idds_api.py",
        "job_api.py",
        "metaconfig_api.py",
        "pilot_api.py",
        "statistics_api.py",
        "system_api.py",
        "task_api.py",
        "workflow_api.py",
    ]
    # Initialize the OpenAPI dictionary
    open_api = {
        "openapi": "3.0.3",
        "servers": [
            {"url": "https://pandaserver.cern.ch/api"},
            {"url": "http://pandaserver.cern.ch/api"},
        ],
        "info": {"title": "PanDA API", "version": "1.0.0", "description": DESCRIPTION},
        "paths": {},
        "tags": [],
    }

    for file_path in file_paths:
        tag = file_path.removesuffix("_api.py")
        open_api["tags"].append(
            {"name": tag, "description": f"Operations related to {tag}"}
        )
        full_path = base_path + file_path
        docstrings = extract_docstrings(full_path)

        # Convert docstrings to OpenAPI
        paths = convert_docstrings_to_openapi(docstrings, tag)
        open_api["paths"].update(paths)

    with open("panda_api.yaml", "w") as output_file:
        yaml.dump(open_api, output_file, sort_keys=False)
