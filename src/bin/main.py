from my_http.server import server_init
from pathlib import Path
from my_http.parser import Request
from my_http.response import Response, NotFound, Unauthorized, Forbidden
from my_http.router import App
import jwt
import uuid
import datetime

app = App()
app.static_folder = Path(__file__).parent.parent.parent / "html_files"

users = {}


@app.route("/hello", "GET")
def get_hello(request: Request) -> str:
    return Response(body="Hello World")


@app.route("/time", "GET")
def get_time(request: Request) -> str:
    return Response(body=str(datetime.datetime.now()))


@app.route("/login", "POST")
def post_login(request: Request) -> Response:
    body = request.body
    for idx in users:
        if (
            body["password"] == users[idx]["password"]
            and body["username"] == users[idx]["username"]
        ):
            authorization_token = jwt.encode(
                {"user_id": idx}, "secret", algorithm="HS256"
            )
            response_headers = {"Set-Cookie": "session=" + authorization_token}
            return Response(headers=response_headers)
    return Response(body=body)


@app.route("/users/{idx:str}", "GET")
def get_users(request: Request) -> Response:
    user = users.get(request.path_params["idx"])
    if user is None:
        return Response(status=NotFound())
    return user


@app.route("/users", "POST")
def post_users(request: Request) -> Response:
    user = request.body
    new_user_id = str(uuid.uuid4())
    users[new_user_id] = user
    return str(new_user_id)


@app.route("/users/{idx:str}", "DELETE")
def delete_users(request: Request) -> Response:
    user_id = request.path_params["idx"]
    if "Authorization" in request.headers:
        encoded_jwt = request.headers["Authorization"].split(" ")[1]
        try:
            decoded_jwt = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
        except jwt.exceptions.InvalidTokenError:
            return Response(status=Unauthorized())

        if user_id in users and decoded_jwt["user_id"] == user_id:
            del users[request.path_params["idx"]]
            return Response(body="User deleted succesfully.")
        else:
            return Response(status=Forbidden())
    else:
        return Response(status=Unauthorized())


@app.route("/users/{idx:str}", "PUT")
def put_users(request: Request) -> Response:
    user_id = request.path_params["idx"]
    if user_id in users:
        users[user_id] = request.body
    else:
        return Response(status=NotFound())

    return Response(body=users[user_id])


@app.route("/users/{idx:str}", "PATCH")
def patch_users(request: Request) -> Response:
    user_id = request.path_params["idx"]
    if user_id in users:
        payload = request.body()
        for key in payload:
            users[user_id][key] = payload[key]
    else:
        return Response(status=NotFound())
    return Response(body=users[user_id])


if __name__ == "__main__":
    server_init(app)
