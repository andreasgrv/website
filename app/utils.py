import os
from flask import Response

from methinks.utils import data_to_json


SECRET_TOKEN = os.environ['METHINKS_TOKEN']


def response(status, msg=None, **kwargs):
    d = dict(status=status,
             message=msg or '',
             **kwargs)
    json_response = data_to_json(d)
    return Response(status=200,
                    response=json_response,
                    mimetype='application/json')


def validate_post(request):
    # First check if request comes from valid IP address
    data = request.get_json()
    st = data.pop('token')
    if st != SECRET_TOKEN:
        raise ValueError('Unauthorised')
    return data


def validate_get(request):
    st = request.args.get('token', type=str)
    if st != SECRET_TOKEN:
        raise ValueError('Unauthorised')
