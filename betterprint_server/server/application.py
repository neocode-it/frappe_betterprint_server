from werkzeug.wrappers import Request, Response

import json
import os

import betterprint_server.global_queue as global_queue


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
    }

    if request.path in route_map:
        response = route_map[request.path](data)
    else:
        response = Response("Not Found", status=404)

    return response(environ, start_response)

    if request.path == "/v1/status":
        response = Response("BETTERPRINT OK", mimetype="text/plain")

    elif request.path == "/v1/calculate-element-heights":
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
                response = Response(body, mimetype="application/json")
            else:
                raise Exception("Unknown exception")

        except Exception as e:
            response = Response(f"Input data invalid: {e}", status="422")

    elif request.path == "/v1/split-table-by-height":
        try:
            if not isinstance(data["html"], str):
                raise ValueError("html must be defined and type string")

            if not isinstance(data["max-height"], int) and data["max-height"] > 0:
                raise ValueError("max-height must be defined and > int 0")

            result = global_queue.queue.run_and_wait("split-table-by-height", data)
            if not result["error"]:
                body = json.dumps(result["content"])
                response = Response(body, mimetype="application/json")
            else:
                raise Exception("Unknown exception")

        except Exception as e:
            response = Response("Input data invalid", status="422")

    elif request.path == "/v1/generate-pdf":
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
                response = Response(body, mimetype="application/json")

            else:
                raise Exception("Unknown exception")

        except Exception as e:
            response = Response(f"Input data invalid: {e}", status="422")

    elif request.path == "/v1/generate-betterprint-pdf":
        try:
            if not isinstance(data["html"], str):
                raise ValueError("'html' is not a str value")

            if not os.path.isabs(data["filepath"]) or os.path.isdir(data["filepath"]):
                raise ValueError("filepath must be absolute path to file")

            result = global_queue.queue.run_and_wait("generate-betterprint-pdf", data)

            if not result["error"]:
                body = json.dumps(result["content"])
                response = Response(body, mimetype="application/json")

            else:
                raise Exception("Unknown exception")

        except Exception as e:
            response = Response(f"Input data invalid: {e}", status="422")
    else:
        response = Response("Not Found", status=404)

    return response(environ, start_response)
