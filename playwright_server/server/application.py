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

    elif request.path == '/v1/calculate-element-heights':
        if (
            type(data) is dict 
            and {'html','element', 'style'} <= data.keys() 
            and type(data['html']) is str 
            and type(data['style']) is str
            and type(data['element']) is str and not data['element'].isspace()
        ):
            result = global_queue.queue.run_and_wait('calculate-element-heights', data)
            if result['error'] == False:
                body = json.dumps(result['content'])
                response = Response(body, mimetype='application/json')
        else:
            response = Response('Input data invalid', status='422')
    
    else:
        response = Response('Not Found', status=404)
    
    return response(environ, start_response)