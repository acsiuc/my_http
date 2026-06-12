from my_http.server import server_init
from pathlib import Path
from my_http.parser import Request
from my_http.response import Response, NotFound
from my_http.router import App
import jwt
import uuid
import datetime

app = App()
app.static_folder = Path(__file__).parent.parent.parent / "html_files"

users = {}


@app.route("/hello", "GET")
def get_hello(request: Request) -> str:
    return "Hello World"


@app.route("/time", "GET")
def get_time(request: Request) -> str:
    return str(datetime.datetime.now())


@app.route("/login", "POST")
def post_login(request: Request) -> Response:
    body = request.json()
    for idx in users:
        if (
            body["password"] == users[idx]["password"]
            and body["username"] == users[idx]["username"]
        ):
            authorization_token = jwt.encode(
                {"user_id": idx}, "secret", algorithm="HS256"
            )
            return Response(body=authorization_token)
    return Response(body=body)


@app.route("/users/{idx:str}", "GET")
def get_users(request: Request) -> Response:
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


@app.route("/users/{idx:str}", "DELETE")
def delete_users(request: Request) -> Response:
    if request.path_params["idx"] in users:
        del users[request.path_params["idx"]]
        return Response(body="User deleted succesfully.")
    else:
        return Response(status=NotFound())


@app.route("/users/{idx:str}", "PUT")
def put_users(request: Request) -> Response:
    user_id = request.path_params["idx"]
    if user_id in users:
        users[user_id] = request.json()
    else:
        return Response(status=NotFound())

    return Response(body=users[user_id])


@app.route("/users/{idx:str}", "PATCH")
def patch_users(request: Request) -> Response:
    user_id = request.path_params["idx"]
    if user_id in users:
        payload = request.json()
        for key in payload:
            users[user_id][key] = payload[key]
    else:
        return Response(status=NotFound())
    return Response(body=users[user_id])


if __name__ == "__main__":
    server_init(app)
