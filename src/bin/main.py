from my_http.server import server_init
from pathlib import Path
from my_http.parser import Request
from my_http.response import Response, NotFound
from my_http.router import App
import uuid
import datetime

app = App()

users = {}


@app.route("/hello", "GET")
def get_hello(request: Request) -> str:
    return "Hello World"


@app.route("/time", "GET")
def get_time(request: Request) -> str:
    return str(datetime.datetime.now())


@app.route("/html", "GET")
def get_html(request: Request) -> dict:
    current_path = Path(__file__)
    html_file_content = current_path.parent.parent.parent / "html_files/index.html"
    with open(html_file_content, "r") as file:
        body = file.read()
    return body


@app.route("/login", "GET")
def get_login(request: Request) -> dict:
    current_path = Path(__file__)
    html_file_content = current_path.parent.parent.parent / "html_files/login.html"
    with open(html_file_content, "r") as file:
        body = file.read()
    return Response(body=body, headers={"Content-Type": "text/html"})


@app.route("/users/{idx:str}", "GET")
def get_user(request: Request) -> Response:
    user = users.get(request.path_params["idx"])
    if user is None:
        return Response(status=NotFound())
    return user


@app.route("/users", "POST")
def post_users(request: Request) -> Response:
    user = request.json()
    new_user_id = str(uuid.uuid4())
    users[new_user_id] = user
    return str(new_user_id)


if __name__ == "__main__":
    server_init(app)
