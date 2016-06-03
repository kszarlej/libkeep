import json
from flask import jsonify

def return_error(err, status):
    data = {
        'status'  : 'error',
        'message' : { 'default': str(err)}
    }
    resp = jsonify(data)
    resp.status_code = status

    return resp

def return_ok():
    data = {
        'status'  : 'ok',
    }
    resp = jsonify(data)
    resp.status_code = 201

    return resp
