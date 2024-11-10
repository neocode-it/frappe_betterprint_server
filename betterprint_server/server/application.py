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
        response = Response("BETTERPRINT OK", mimetype="text/plain")

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
        try:
            if not isinstance(data["html"], str):
                raise ValueError("'html' is not a str value")

            if not os.path.isabs(data["filepath"]) or os.path.isdir(data["filepath"]):
                raise ValueError("filepath must be absolute path to file")

            if "page-width" in data and not data["page-width"] > 0:
                raise ValueError("page width must be int and > 0")

            if "page-height" in data and not data["page-height"] > 0:
                raise ValueError("page height must be int and > 0")

            data["cookies"] = sanitize_cookies(data.get("cookies", []))

            result = global_queue.queue.run_and_wait("generate-pdf", data)

            if not result["error"]:
                body = json.dumps(result["content"])
                response = Response(body, mimetype="application/json")

        except Exception as e:
            response = Response(f"Input data invalid: {e}", status="422")

    else:
        response = Response("Not Found", status=404)

    return response(environ, start_response)


def sanitize_cookies(cookies):
    """
    Will sanitize cookies acoording to the format required by playwright

    Raise Exception if the format is invalid or keys are missing
    """
    san_cookies = []

    for cookie in cookies:
        san_cookie = {
            "name": str(cookie["name"]),
            "value": str(cookie["value"]),
            "domain": str(cookie["domain"]),
            "path": str(cookie["path"]),
        }

        san_cookies.append(san_cookie)

    return san_cookie
