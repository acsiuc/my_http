from dataclasses import dataclass, field
import datetime
import mimetypes
from pathlib import Path
from typing import Callable

from my_http.response import Response

from .parser import Request


@dataclass
class App:
    dictionary_of_paths: dict[str, Callable] = field(default_factory=dict)

    def route(self, path, method):
        def write_to_dict(func):
            if path not in self.dictionary_of_paths:
                self.dictionary_of_paths[path] = {method: func}
            else:
                self.dictionary_of_paths[path][method] = func
            return func
        return write_to_dict


def router(request: Request, dictionary_of_paths: dict[str, Callable]) -> Response:
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
