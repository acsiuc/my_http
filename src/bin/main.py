from my_http.server import server_init


def hello():
    return "Hello World"


dictionary_of_paths = {"/hello": hello}

if __name__ == "__main__":
    server_init(dictionary_of_paths)
