from .parser import Request


def router(request: Request, dictionary_of_paths: dict) -> str:
    if request.path in dictionary_of_paths:
        methods_dictionary = dictionary_of_paths[request.path]
    else:
        return "Path not found."
    if request.method in methods_dictionary:
        response = methods_dictionary[request.method]()
    else:
        return "405 Method Not Allowed"

    return response
