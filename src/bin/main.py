import datetime
from pathlib import Path
import uuid

from my_http.parser import Request
from my_http.response import NotFound, Response, Status
from my_http.router import App, dictionary_of_paths
from my_http.server import server_init

app = App()
users = {
    1: {
        "name": "florin",
    },
    2: {
        "name": "hsc",
    },
}


@app.route("/hello", "GET")
def get_hello(request: Request) -> Response:
    return "Hello"


@app.route("/users/{idx:int}", "GET")
def get_user(request: Request) -> Response:
    user_base, user_idx = request.path
    user = users.get(user_idx)
    if user is None:
        return NotFound
    return user


@app.route("/time", "GET")
def get_time(_) -> Response:
    return str(datetime.datetime.now())


@app.route("/html", "GET")
def get_html(request: Request) -> Response:
    # TODO: maybe look at inspect - a python library
    current_path = Path(__file__)
    html_file_content = current_path.parent.parent.parent / "html_files/index.html"
    with open(html_file_content, "r") as file:
        body = file.read()
    return Response(Status.OK, body)


@app.route("/login", "GET")
def get_login(request: Request) -> Response:
    current_path = Path(__file__)
    html_file_content = current_path.parent.parent.parent / "html_files/login.html"
    with open(html_file_content, "r") as file:
        body = file.read()
    return Response(Status.OK, body)


@app.route("/users", "POST")
def post_login(request: Request) -> Response:
    user = request.json()
    new_user_id = uuid.uuid4()
    users[new_user_id] = user
    return new_user_id


if __name__ == "__main__":
    server_init(dictionary_of_paths)
