from my_http.server import server_init


def get_hello():
    return "I just wanna fuck."


dictionary_of_paths = {"/hello": {"GET": get_hello}}

if __name__ == "__main__":
    server_init(dictionary_of_paths)
