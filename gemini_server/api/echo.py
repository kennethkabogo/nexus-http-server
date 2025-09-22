from ..server import json_response, validate_json


@validate_json({'message': {'type': 'string'}, 'count': {'type': 'integer'}})
def echo_data(request):
    return json_response({'received_data': request.data})