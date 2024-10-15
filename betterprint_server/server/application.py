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

    if request.path == "/v1/status":
        response = Response("PLAYWRIGHT OK", mimetype="text/plain")

    elif request.path == "/v1/calculate-element-heights":
        if (
            type(data) is dict
            and {"html", "element"} <= data.keys()
            and type(data["html"]) is str
            and type(data["element"]) is str
            and not data["element"].isspace()
        ):
            result = global_queue.queue.run_and_wait("calculate-element-heights", data)
            if not result["error"]:
                body = json.dumps(result["content"])
                response = Response(body, mimetype="application/json")
        else:
            response = Response("Input data invalid", status="422")

    elif request.path == "/v1/split-table-by-height":
        if (
            type(data) is dict
            and {"html", "max-height"} <= data.keys()
            and isinstance(data["html"], str)
            and isinstance(data["max-height"], int)
            and data["max-height"] > 0
        ):
            result = global_queue.queue.run_and_wait("split-table-by-height", data)
            if not result["error"]:
                body = json.dumps(result["content"])
                response = Response(body, mimetype="application/json")
        else:
            response = Response("Input data invalid", status="422")

    elif request.path == "/v1/generate-pdf":
        if (
            type(data) is dict
            and {"html", "filepath"} <= data.keys()
            and type(data["html"]) is str
            and type(data["filepath"]) is str
            and os.path.isabs(data["filepath"])
            and not os.path.isdir(data["filepath"])
        ):
            data = {"page_size": "A4", **data}
            valid_paperformats = [
                "Letter",
                "Legal",
                "Tabloid" "Ledger",
                "A0",
                "A1",
                "A2",
                "A3",
                "A4",
                "A5",
                "A6",
            ]
            if data["page_size"] not in valid_paperformats:
                response = Response("Paper format invalid.", status="422")
            else:
                result = global_queue.queue.run_and_wait("generate-pdf", data)
                if not result["error"]:
                    body = json.dumps(result["content"])
                    response = Response(body, mimetype="application/json")
        else:
            response = Response("Input data invalid", status="422")

    else:
        response = Response("Not Found", status=404)

    return response(environ, start_response)
