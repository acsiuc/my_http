from my_http.server import server_init
from pathlib import Path
from my_http.response import Response
from my_http.parser import Request
from my_http.router import dictionary_of_paths, route
import urllib.parse
import datetime


@route("/hello", "GET")
def get_hello(request: Request) -> Response:
    status_line = "HTTP/1.1 200 OK"
    body = "Hello World"
    headers = [
        f"Date: {datetime.datetime.now()}",
        "Content-Type: text",
        f"Content-Length: {len(body)}",
    ]

    return Response(status_line, headers, body)


@route("/time", "GET")
def get_time(request: Request) -> Response:
    status_line = "HTTP/1.1 200 OK"
    body = str(datetime.datetime.now())
    headers = [
        f"Date: {datetime.datetime.now()}",
        "Content-Type: text",
        f"Content-Length: {len(body)}",
    ]

    return Response(status_line, headers, body)


@route("/html", "GET")
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


@route("/login", "GET")
def get_login(request: Request) -> Response:
    status_line = "HTTP/1.1 200 OK"
    current_path = Path(__file__)
    html_file_content = current_path.parent.parent.parent / "html_files/login.html"
    with open(html_file_content, "r") as file:
        body = file.read()
    headers = [
        f"Date: {datetime.datetime.now()}",
        "Content-Type: text/html",
        f"Content-Length: {len(body)}",
    ]
    return Response(status_line, headers, body)


@route("/login", "POST")
def post_login(request: Request) -> Response:
    status_line = "HTTP/1.1 200 OK"
    body = str(urllib.parse.parse_qs(request.body))
    headers = [
        f"Date: {datetime.datetime.now()}",
        "Content-Type: text/html",
        f"Content-Length: {len(body)}",
    ]

    return Response(status_line, headers, body)


if __name__ == "__main__":
    server_init(dictionary_of_paths)
