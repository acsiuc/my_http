from dataclasses import dataclass, field


@dataclass
class StatusCode:
    code: int

    def phrase(self) -> str:
        return "Message"


@dataclass
class OK(StatusCode):
    code: int = 200

    def phrase(self) -> str:
        return "OK"


@dataclass
class NotFound(StatusCode):
    code: int = 404

    def phrase(self) -> str:
        return "Not Found"


@dataclass
class Response:
    status: StatusCode = field(default_factory=OK)
    headers: dict = field(default_factory=dict)
    body: dict | str = field(default="")

    def get_status_line(self) -> str:
        status_line = f"HTTP/1.1 {self.status.code} {self.status.phrase()}"
        return status_line


# def response(response: Response) -> bytes:
#     status_line = response.status_line + "\r\n"
#     headers = "\r\n".join(response.headers)
#     body = "\r\n\r\n" + response.body

#     http_response = status_line + headers + body

#     return http_response.encode()
