from .parser import Request
from my_http.response import Response
from pathlib import Path
import datetime
import mimetypes

dictionary_of_paths = {}


def route(path, method):
    def write_to_dict(func):
        if path not in dictionary_of_paths:
            dictionary_of_paths[path] = {method: func}
        else:
            dictionary_of_paths[path][method] = func
        return func

    return write_to_dict


def router(request: Request, dictionary_of_paths: dict) -> Response:
    current_path = Path(__file__)
    path = current_path.parent.parent.parent / f"html_files{request.path}"
    path_exists = Path.is_file(path)
    if request.path in dictionary_of_paths:
        methods_dictionary = dictionary_of_paths[request.path]
    elif path_exists:
        with open(path, "r") as f:
            body = f.read()
        status_line = "HTTP/1.1 200 OK"
        file_type = mimetypes.guess_type(path)[0] or "text/plain"
        headers = [
            f"Date: {datetime.datetime.now()}",
            f"Content-Type: {file_type}",
            f"Content-Length: {len(body)}",
        ]
        return Response(status_line, headers, body)
    else:
        return Response("HTTP/1.1 404 Not Found", [], "Error 404. Not Found")

    if request.method in methods_dictionary:
        response = methods_dictionary[request.method](request)
    else:
        return Response(
            "HTTP/1.1 405 Method Not Allowed", [], "Error 405. Method Not Allowed"
        )

    return response
