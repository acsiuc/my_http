from my_http.server import server_init
from pathlib import Path
from my_http.response import Response
from my_http.parser import Request
import datetime
import json


def get_hello(request: Request) -> Response:
    status_line = "HTTP/1.1 200 OK"
    body = "Hello World"
    headers = [
        f"Date: {datetime.datetime.now()}",
        "Content-Type: text",
        f"Content-Length: {len(body)}",
    ]

    return Response(status_line, headers, body)


def get_time(request: Request) -> Response:
    status_line = "HTTP/1.1 200 OK"
    body = str(datetime.datetime.now())
    headers = [
        f"Date: {datetime.datetime.now()}",
        "Content-Type: text",
        f"Content-Length: {len(body)}",
    ]

    return Response(status_line, headers, body)


def get_html(request: Request) -> Response:
    status_line = "HTTP/1.1 200 OK"
    current_path = Path(__file__)
    html_file_content = current_path.parent.parent.parent / "html_files/index.html"
    with open(html_file_content, "r") as file:
        body = file.read()
    headers = [
        f"Date: {datetime.datetime.now()}",
        "Content-Type: text/html",
        f"Content-Length: {len(body)}",
    ]
    return Response(status_line, headers, body)


def post_login(request: Request) -> Response:
    status_line = "HTTP/1.1 200 OK"
    body = json.dumps(json.loads(request.body))
    headers = [
        f"Date: {datetime.datetime.now()}",
        "Content-Type: text/html",
        f"Content-Length: {len(body)}",
    ]

    return Response(status_line, headers, body)


dictionary_of_paths = {
    "/hello": {"GET": get_hello},
    "/time": {"GET": get_time},
    "/html": {"GET": get_html},
    "/login": {"POST": post_login},
}

if __name__ == "__main__":
    server_init(dictionary_of_paths)
