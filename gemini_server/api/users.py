from ..server import require_auth, json_response


@require_auth
def get_users(request):
    users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
    return json_response({'users': users, 'authenticated_user': request.user})