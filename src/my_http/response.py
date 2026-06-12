from dataclasses import dataclass, field
from datetime import timezone
import datetime
import json


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
class NotAllowed(StatusCode):
    code: int = 405

    def phrase(self) -> str:
        return "Method Not Allowed"


@dataclass
class Unauthorized(StatusCode):
    code: int = 401

    def phrase(self) -> str:
        return "Unauthorized"


@dataclass
class Forbidden(StatusCode):
    code: int = 403

    def phrase(self) -> str:
        return "Forbidden"


@dataclass
class Response:
    status: StatusCode = field(default_factory=OK)
    headers: dict = field(default_factory=dict)
    body: dict | str = field(default="")

    def get_status_line(self) -> str:
        status_line = f"HTTP/1.1 {self.status.code} {self.status.phrase()}"
        return status_line

    def encode(self) -> bytes:
        status_line = self.get_status_line() + "\r\n"
        if isinstance(self.body, dict):
            body = json.dumps(self.body)
            if "Content-Type" not in self.headers:
                self.headers["Content-Type"] = "application/json"
        else:
            body = self.body
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "text/plain"
        self.headers["Content-Length"] = len(body)
        self.headers["Date"] = datetime.datetime.now(timezone.utc).strftime(
            "%a, %d %b %Y %H:%M:%S GMT"
        )
        headers = "\r\n".join(f"{key}: {value}" for key, value in self.headers.items())

        http_response = status_line + headers + "\r\n\r\n" + body

        return http_response.encode()
