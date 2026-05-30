class Request:
    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body


def parse(unparsed_data: bytes) -> Request:
    parsed_data = unparsed_data.decode()
    split_data = parsed_data.split("\r\n\r\n")
    if len(split_data) < 2:
        raise ValueError
    request_and_headers = split_data[0].split("\r\n")
    request = request_and_headers[0].split(" ")
    if len(request) != 3:
        raise ValueError
    method = request[0]
    path = request[1]
    headers = request_and_headers[1:]
    try:
        body = split_data[1]
    except IndexError:
        body = ""
    object_to_return = Request(method, path, headers, body)

    return object_to_return
