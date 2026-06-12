from dataclasses import dataclass, field
import json


@dataclass
class Request:
    method: str
    path: str = field(default="")
    headers: dict = field(default_factory=dict)
    body: str = field(default="")
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
            headers[header_and_content[0]] = header_and_content[1]

        body = split_data[1]

        obj = cls(method, path, headers, body)

        return obj

    def json(self):
        return json.loads(self.body)
