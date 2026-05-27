from .parser import Request
from my_http.response import Response


def router(request: Request, dictionary_of_paths: dict) -> Response:
    if request.path in dictionary_of_paths:
        methods_dictionary = dictionary_of_paths[request.path]
    else:
        return Response("HTTP/1.1 404 Not Found", [], "Error 404. Not Found")

    if request.method in methods_dictionary:
        response = methods_dictionary[request.method]()
    else:
        return Response(
            "HTTP/1.1 405 Method Not Allowed", [], "Error 405. Method Not Allowed"
        )

    return response
