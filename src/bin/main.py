from my_http.server import server_init
import datetime


def get_hello():
    return "Hello world."


def get_time():
    return str(datetime.datetime.now())


dictionary_of_paths = {"/hello": {"GET": get_hello}, "/time": {"GET": get_time}}

if __name__ == "__main__":
    server_init(dictionary_of_paths)
