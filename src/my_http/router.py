from .parser import Request
from my_http.response import Response, NotFound, NotAllowed
from typing import Callable
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class App:
    dictionary_of_paths: dict[str, dict[str, Callable]] = field(default_factory=dict)
    static_file: str = field(default=None)

    def route(self, path, method):
        def write_to_dict(func):
            if path not in self.dictionary_of_paths:
                self.dictionary_of_paths[path] = {method: func}
            else:
                self.dictionary_of_paths[path][method] = func
            return func

        return write_to_dict

    def send_static_file(self, filename):
        if not self.static_file:
            raise RuntimeError("static_files must be set")
        with open(Path(self.static_file) / filename, "r") as f:
            body = f.read()
        return Response(body=body)

    def router(self, request: Request) -> Response:
        path_exists = Path.is_file(Path(self.static_file) / request.path)

        if request.path in self.dictionary_of_paths:
            methods_dictionary = self.dictionary_of_paths[request.path]
        elif path_exists:
            return self.send_static_file(request.path)
        else:
            return Response(status=NotFound(), body="Error 404. Not Found")

        if request.method in methods_dictionary:
            response = methods_dictionary[request.method](request)
            if isinstance(response, Response):
                return response
            else:
                return Response(body=response)
        else:
            return Response(status=NotAllowed(), body="Error 405. Method Not Allowed")
