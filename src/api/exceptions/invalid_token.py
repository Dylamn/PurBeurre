class InvalidToken(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super(InvalidToken, self).__init__()
        self.message = message

        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_response(self):
        body = dict(self.payload or ())
        body['message'] = self.message

        return body
