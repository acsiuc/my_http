from .parser import Request


def router(request: Request, dictionary_of_paths: dict) -> str:
    if request.path in dictionary_of_paths:
        response = dictionary_of_paths[request.path]()
    else:
        return "Path not found."

    return response
