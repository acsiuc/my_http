from .parser import Request
from my_http.response import Response, NotFound, NotAllowed
from typing import Callable
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class App:
    dictionary_of_paths: dict[str, dict[str, Callable]] = field(default_factory=dict)
    static_folder: str = field(default=None)

    TYPE_MAP = {
        "int": int,
        "str": str,
    }

    def route(self, path, method):
        def write_to_dict(func):
            if path not in self.dictionary_of_paths:
                self.dictionary_of_paths[path] = {method: func}
            else:
                self.dictionary_of_paths[path][method] = func
            return func

        return write_to_dict

    def send_static_file(self, filename):
        if not self.static_folder:
            raise RuntimeError("static_files must be set")
        with open(Path(self.static_folder) / filename.lstrip("/"), "r") as f:
            body = f.read()
        return Response(body=body, headers={"Content-Type": "text/html"})

    def router(self, request: Request) -> Response:
        if self.static_folder:
            path_exists = Path.is_file(
                Path(self.static_folder) / request.path.lstrip("/")
            )
        else:
            path_exists = False
        methods_dictionary = {}

        for path in self.dictionary_of_paths:
            if path == request.path:
                methods_dictionary = self.dictionary_of_paths[path]
            elif len(path.split("/")) == len(request.path.split("/")):
                to_match = path.split("/")
                for i in range(len(path.split("/"))):
                    if (
                        not to_match[i] == request.path.split("/")[i]
                        and "{" not in to_match[i]
                    ):
                        break
                    elif (
                        "{" in to_match[i]
                        and to_match[i].strip("{}").split(":")[1] in self.TYPE_MAP
                    ):
                        try:
                            request.path_params[
                                to_match[i].strip("{}").split(":")[0]
                            ] = self.TYPE_MAP[to_match[i].strip("{}").split(":")[1]](
                                request.path.split("/")[i]
                            )
                        except ValueError:
                            break
                else:
                    methods_dictionary = self.dictionary_of_paths[path]

        if methods_dictionary:
            if request.method == "HEAD":
                if "GET" in methods_dictionary:
                    response = methods_dictionary["GET"](request)
                    print(response.body)
                    response.headers["Content-Length"] = len(response.body)
                    response.body = ""
                    print(response.body)
                    return response
                else:
                    return Response(status=NotAllowed())
            elif request.method in methods_dictionary:
                response = methods_dictionary[request.method](request)
                if isinstance(response, Response):
                    return response
                else:
                    return Response(body=response)
            else:
                return Response(
                    status=NotAllowed(), body="Error 405. Method Not Allowed"
                )
        elif not methods_dictionary:
            if path_exists:
                return self.send_static_file(request.path)
            else:
                return Response(status=NotFound(), body="Error 404. Not Found")
