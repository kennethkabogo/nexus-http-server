import json


def json_response(data, status='200 OK'):
    headers = [('Content-type', 'application/json')]
    return status, headers, json.dumps(data)


def redirect(url, status='302 Found'):
    headers = [('Location', url)]
    return status, headers, ''