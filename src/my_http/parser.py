from dataclasses import dataclass, field
import json


@dataclass
class Request:
    method: str
    path: str = field(default="")
    headers: dict = field(default_factory=dict)
    body: dict | str = field(default="")
    path_params: dict = field(default_factory=dict)

    @classmethod
    def parse(cls, unparsed_data: bytes) -> Request:
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
        auxiliary_headers = request_and_headers[1:]
        headers = {}
        for header in auxiliary_headers:
            header_and_content = header.split(":", 1)
            headers[header_and_content[0]] = header_and_content[1].lstrip()

        body = split_data[1]

        obj = cls(method, path, headers, body)

        return obj

    def parse_by_type(self):
        headers = self.headers
        body = self.body
        if "Content-Type" in headers:
            if headers["Content-Type"] == "application/json":
                self.body = json.loads(body)
            elif headers["Content-Type"] == "application/x-www-form-urlencoded":
                key_value_pairs = body.split("&")
                body = {}
                for pair in key_value_pairs:
                    key = pair.split("=")[0]
                    value = pair.split("=")[1]
                    body[key] = value
                self.body = body

    def json(self):
        return json.loads(self.body)
