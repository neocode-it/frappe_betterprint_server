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

    # Set default response
    response = Response('Internal server error', status=500)
    
    if request.path == '/v1/status':
        response = Response('PLAYWRIGHT OK', mimetype='text/plain')

    else:
        response = Response('Not Found', status=404)
    
    return response(environ, start_response)