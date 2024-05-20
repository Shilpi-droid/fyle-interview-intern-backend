from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))

    @staticmethod
    def respond_error_with_details(message=None, status_code=400, error=None):
        response = {
            'status': 'error',
            'message': message,
            'error': error
        }
        return jsonify(response), status_code