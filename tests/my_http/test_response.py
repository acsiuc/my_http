from my_http.response import Response, NotFound


def test_ok_status_line():
    response = Response(body="Hello")
    assert response.get_status_line() == "HTTP/1.1 200 OK"


def test_not_found_status_line():
    response = Response(status=NotFound(), body="Not Found")
    assert response.get_status_line() == "HTTP/1.1 404 Not Found"
