from my_http.parser import parse
import pytest


def test_parse_no_errors():
    string = "Bine"
    http_request = (
        f"GET /hello HTTP/1.1\r\nContent-Length: 4\r\nContent-Type: text/html\r\n\r\n{string}"
    ).encode()

    assert parse(http_request).method == "GET"
    assert parse(http_request).path == "/hello"
    assert parse(http_request).headers == [
        "Content-Length: 4",
        "Content-Type: text/html",
    ]
    assert parse(http_request).body == string


def test_parse_no_body():
    http_request = (
        "GET /hello HTTP/1.1\r\nContent-Length: 4\r\nContent-Type: text/html\r\n\r\n"
    ).encode()

    assert parse(http_request).method == "GET"
    assert parse(http_request).path == "/hello"
    assert parse(http_request).headers == [
        "Content-Length: 4",
        "Content-Type: text/html",
    ]
    assert parse(http_request).body == ""


def test_malformed_request():
    http_request = "GET GET//HEllo HHHH TTPP".encode()

    with pytest.raises(ValueError):
        assert parse(http_request)


def test_no_headers():
    string = "Bine"
    http_request = (f"GET /hello HTTP/1.1\r\n\r\n\r\n{string}").encode()

    assert parse(http_request).headers == []
