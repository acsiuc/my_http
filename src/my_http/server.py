import socket
from .parser import parse
from .router import router


def server_init(dictionary_of_paths: dict):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(("", 8080))
    my_socket.listen(5)

    while True:
        connection_socket, address = my_socket.accept()
        unparsed_data = b""
        while b"\r\n\r\n" not in unparsed_data:
            unparsed_data += connection_socket.recv(1024)
        if len(unparsed_data) != 0:
            parsed_data = parse(unparsed_data)
        else:
            connection_socket.close()
            continue
        if "Content-Length" in "".join(parsed_data.headers):
            for x in parsed_data.headers:
                if "Content-Length" in x:
                    body_length = int(x.split(":")[1].strip())
                    while len(parsed_data.body) < body_length:
                        parsed_data.body += connection_socket.recv(body_length).decode()
        else:
            parsed_data.body = ""
        method_result = router(parsed_data, dictionary_of_paths)
        # TODO: based on the returned value create appropriate response

        connection_socket.send(method_result.encode())
        connection_socket.close()
