class Response:
    def __init__(self, status_line, headers: list, body: str):
        self.status_line = status_line
        self.headers = headers
        self.body = body


def response(response: Response) -> bytes:
    status_line = response.status_line + "\r\n"
    headers = "\r\n".join(response.headers)
    body = "\r\n\r\n" + response.body

    http_response = status_line + headers + body

    return http_response.encode()
