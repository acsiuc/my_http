def response(routed_content: str) -> bytes:
    status_line = "HTTP/1.1 200 OK\r\n"
    header = f"Content-Length: {len(routed_content)}"
    body = f"\r\n\r\n{routed_content}"

    http_response = status_line + header + body

    return http_response.encode()
