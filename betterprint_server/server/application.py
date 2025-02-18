from werkzeug.wrappers import Request, Response

import json
import os

import betterprint_server.global_queue as global_queue
from betterprint_server.server.validation import validate
import betterprint_server.server.validation as validation


def application(environ, start_response):
    request = Request(environ)
    # Parse json
    data = None
    lenght = len(request.get_data())
    if lenght and lenght < 10_000_000:
        data = request.get_json()

    # Set default response
    response = Response("Internal server error", status=500)

    route_map = {
        "/v1/status": status,
        "/v1/calculate-element-heights": calculate_element_height,
        "/v1/generate-pdf": generate_pdf,
        "/v1/split-table-by-height": split_table_by_height,
        "/v1/generate-betterprint-pdf": generate_betterprint_pdf,
    }

    if request.path in route_map:
        response = route_map[request.path](data)
    else:
        response = Response("Not Found", status=404)

    return response(environ, start_response)


def status(data):
    return Response("BETTERPRINT OK", mimetype="text/plain")


def calculate_element_height(data):
    try:
        input_data = {
            "html": str(data["html"]),
            "element": str(data["element"]),
        }

        result = global_queue.queue.run_and_wait(
            "calculate-element-heights", input_data
        )

        if not result["error"]:
            body = json.dumps(result["content"])
            return Response(body, mimetype="application/json")
        else:
            raise Exception("Unknown exception")

    except Exception as e:
        return Response(f"Input data invalid: {e}", status="422")


def generate_pdf(data):
    try:
        if not isinstance(data["html"], str):
            raise ValueError("'html' is not a str value")

        if not os.path.isabs(data["filepath"]) or os.path.isdir(data["filepath"]):
            raise ValueError("filepath must be absolute path to file")

        if "page-width" in data and not data["page-width"] > 0:
            raise ValueError("page width must be int and > 0")

        if "page-height" in data and not data["page-height"] > 0:
            raise ValueError("page height must be int and > 0")

        result = global_queue.queue.run_and_wait("generate-pdf", data)

        if not result["error"]:
            body = json.dumps(result["content"])
            return Response(body, mimetype="application/json")

        else:
            raise Exception("Unknown exception")

    except Exception as e:
        return Response(f"Input data invalid: {e}", status="422")


def split_table_by_height(data):
    try:
        if not isinstance(data["html"], str):
            raise ValueError("html must be defined and type string")

        if not isinstance(data["max-height"], int) and data["max-height"] > 0:
            raise ValueError("max-height must be defined and > int 0")

        result = global_queue.queue.run_and_wait("split-table-by-height", data)
        if not result["error"]:
            body = json.dumps(result["content"])
            return Response(body, mimetype="application/json")
        else:
            raise Exception("Unknown exception")

    except Exception as e:
        return Response("Input data invalid", status="422")


def generate_betterprint_pdf(data):
    errors = validate(
        data,
        {
            "filepath": [validation.is_valid_pdf_filepath],
            "origin": [validation.is_valid_url],
            "html": [validation.is_valid_string],
        },
    )

    if errors:
        response = {"status": "failed", "errors": errors}
        return Response(json.dumps(response), mimetype="application/json", status="422")

    result = global_queue.queue.run_and_wait("generate-betterprint-pdf", data)

    if "error" in result:
        return Response(f"Input data invalid: {result['error']}", status="422")

    body = json.dumps(result["content"])
    return Response(body, mimetype="application/json")
