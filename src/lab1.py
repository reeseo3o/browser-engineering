import socket
import ssl
import wbetools

class URL:
    def __init__(self, url):
        try:
            print(f"[URL] Parsing URL: {url}")
            self.scheme, url = url.split("://", 1)
            assert self.scheme in ["http", "https"]
            print(f"[URL] Scheme: {self.scheme}")

            if "/" not in url:
                url = url + "/"
            self.host, url = url.split("/", 1)
            self.path = "/" + url
            print(f"[URL] Host: {self.host}, Path: {self.path}")

            if self.scheme == "http":
                self.port = 80
            elif self.scheme == "https":
                self.port = 443

            if ":" in self.host:
                self.host, port = self.host.split(":", 1)
                self.port = int(port)
            print(f"[URL] Port: {self.port}")
        except:
            print("Malformed URL found, falling back to the WBE home page.")
            print("  URL was: " + url)
            self.__init__("https://browser.engineering")

    def request(self):
        print(f"[REQUEST] Creating socket connection to {self.host}:{self.port}")
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        s.connect((self.host, self.port))
        print(f"[REQUEST] Connected successfully")

    # ssl 래핑(HTTPS 프로토콜 사용 시)
        if self.scheme == "https":
            print(f"[REQUEST] Wrapping socket with SSL/TLS")
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "\r\n"
        print(f"[REQUEST] Sending HTTP request:\n{request.strip()}")

        s.send(request.encode("utf8"))
        response = s.makefile("r", encoding="utf8", newline="\r\n")

        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)
        print(f"[RESPONSE] Status line: {version} {status} {explanation.strip()}")

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        print(f"[RESPONSE] Headers: {len(response_headers)} headers received")
        for key, value in list(response_headers.items())[:5]:
            print(f"[RESPONSE]   {key}: {value}")

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        print(f"[RESPONSE] Body: {len(content)} characters received")
        s.close()

        return content

    @wbetools.js_hide
    def __repr__(self):
        return "URL(scheme={}, host={}, port={}, path={!r})".format(
            self.scheme, self.host, self.port, self.path)

def show(body):
    print("\n[SHOW] Displaying content (HTML tags removed):")
    print("=" * 60)
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")
    print("\n" + "=" * 60)

def load(url):
    body = url.request()
    show(body)

if __name__ == "__main__":
    import sys
    load(URL(sys.argv[1]))

# python lab1.py http://example.org
# python lab1.py https://browser.engineering/http.html
# python lab1.py https://ui.shadcn.com/