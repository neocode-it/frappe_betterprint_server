from werkzeug.wrappers import Request, Response

import json
import os

import playwright_server.global_queue as global_queue

def application(environ, start_response):
    request = Request(environ)
    # Parse json
    data = None
    lenght = len(request.get_data())
    if lenght and lenght < 10_000_000:
        data = request.get_json()


    else:
        response = Response('Not Found', status=404)
    
    return response(environ, start_response)