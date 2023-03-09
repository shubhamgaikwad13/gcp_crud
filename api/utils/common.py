from http import HTTPStatus
from flask import make_response, jsonify


def json_response(message=None, data=None, data_key=None, status=HTTPStatus.OK):
    response = dict()

    if message is not None:
        response.update({'message': message})
    if data is not None:
        response.update({data_key if data_key else 'data': data})

    # return make_response(jsonify({'message': message, 'data': data}), status)
    return make_response(jsonify(response), status)


def error_response(message="An error occured", status=HTTPStatus.INTERNAL_SERVER_ERROR):
    return make_response(jsonify({'error': str(message)}), status)
