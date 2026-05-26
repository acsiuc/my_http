import socket
from .parser import parse
from .router import router
from .response import response


def server_init(dictionary_of_paths: dict):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(("", 8080))
    my_socket.listen(5)

    while True:
        connection_socket, address = my_socket.accept()
        unparsed_data = b""
        while b"\r\n\r\n" not in unparsed_data:
            unparsed_data += connection_socket.recv(1024)
        parsed_data = parse(unparsed_data)
        routed_content = router(parsed_data, dictionary_of_paths)
        connection_socket.send(response(routed_content))
        connection_socket.close()
