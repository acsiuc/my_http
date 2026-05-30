from dataclasses import dataclass, field


class Status:
    OK = 200
    NOT_FOUND = 404


@dataclass
class Response:
    status: Status = field()
    body: dict | str = field(default=None)
    headers: dict = field(default_factory=dict)
    status_line: str = field(default=None)

    def encode(self) -> bytes:
        status_line = self.status_line + "\r\n"
        headers = "\r\n".join(self.headers)
        body = "\r\n\r\n" + self.body

        http_response = status_line + headers + body

        return http_response.encode()

    def eoncode_it(self) -> bytes:
        status_line = "HTTP/1.1 200 OK"
        body = str(datetime.datetime.now())
        headers = [
            f"Date: {datetime.datetime.now()}",
            "Content-Type: text",
            f"Content-Length: {len(body)}",
        ]
        self.encode()
        return "payload"  #


class NotFound:
    pass
