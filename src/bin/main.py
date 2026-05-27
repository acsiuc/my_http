from my_http.server import server_init
from pathlib import Path
from my_http.response import Response
import datetime


def get_hello() -> Response:
    status_line = "HTTP/1.1 200 OK"
    body = "Hello World"
    headers = [
        f"Date: {datetime.datetime.now()}",
        "Content-Type: text",
        f"Content-Length: {len(body)}",
    ]

    return Response(status_line, headers, body)


def get_time():
    return str(datetime.datetime.now())


def get_html():
    current_path = Path(__file__)
    html_file_content = current_path.parent.parent.parent / "html_files/index.html"
    with open(html_file_content, "r") as file:
        return file.read()


dictionary_of_paths = {
    "/hello": {"GET": get_hello},
    "/time": {"GET": get_time},
    "/html": {"GET": get_html},
}

if __name__ == "__main__":
    server_init(dictionary_of_paths)
