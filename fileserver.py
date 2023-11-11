def run(port=80, pwd=""):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from socket import gethostbyname_ex, gethostname
    from urllib.parse import unquote
    import json
    import os
    import time

    SERVER_NAME = "Shiro-chan"

    PATH_INDEX = "./lib/index.html"
    PATH_SAMPLE = "./lib/sample.html"
    PATH_ROOT = ".."

    FILTER = ["MP4", "MOV", "MKV"]

    class SuperHTTPServer(BaseHTTPRequestHandler):

        def send_server_info(self):
            self.send_header("Connection", "close")
            self.send_header("Date", time.strftime("%Y.%m.%d %H:%M:%S %z"))
            self.send_header("Server", SERVER_NAME)

        def response403(self):
            self.send_response_only(403, "Forbidden")
            self.send_server_info()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": False,
                "status_code": 403,
                "message": "未授权访问"
            }, ensure_ascii=False).encode("utf-8"))

        def response404(self):
            self.send_response_only(404, "Not Found")
            self.send_server_info()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": False,
                "status_code": 404,
                "message": "找不到请求的资源"
            }, ensure_ascii=False).encode("utf-8"))

        def response500(self):
            self.send_response_only(500, "Internal Server Error")
            self.send_server_info()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "ok": False,
                "status_code": 500,
                "message": "服务器错误"
            }, ensure_ascii=False).encode("utf-8"))

        def response200(self):
            self.send_response_only(200, "OK")
            self.send_server_info()
            self.send_header("Server", SERVER_NAME)

        def IsAccessible(self, path):
            accessible = [f"/{x}" for x in os.listdir(f"{PATH_ROOT}") if os.path.isfile(f"{PATH_ROOT}/{x}") and not x.startswith(".") and x.split(".")[-1].upper() in FILTER] + ["./lib/icon.png"]
            if path in accessible:
                return True
            else:
                return False

        def sendfile(self, path):
            try:
                if path == "/lib/icon.png":
                    with open(f".{path}", "rb") as f:
                        c = f.read()
                else:
                    with open(f"{PATH_ROOT}{path}", "rb") as f:
                        c = f.read()

                self.response200()
                self.send_header("Content-Type", "application/file; charset=utf-8")
                self.send_header("Content-Length", str(len(c)))
                self.end_headers()
                self.wfile.write(c)
            except:
                self.response500()

        def sendpage(self):
            try:
                with open(PATH_INDEX, "rt") as f:
                    index = f.read()
                with open(PATH_SAMPLE, "rt") as f:
                    sample = f.read()

                page = index.split("{{BREAKPOINT}}")[0]

                for filename in sorted([x for x in os.listdir(f"{PATH_ROOT}") if os.path.isfile(f"{PATH_ROOT}/{x}") and not x.startswith(".") and x.split(".")[-1].upper() in FILTER]):
                    filetime = time.strftime("%m/%d %H:%M", time.localtime(os.path.getctime(f"{PATH_ROOT}/{filename}")))
                    filesize = f"{os.path.getsize(f'{PATH_ROOT}/{filename}')/10**6:.1f} MB"
                    filetype = filename.split(".")[-1].upper()

                    label = sample.replace("{{FILENAME}}", filename).replace("{{FILETIME}}", filetime).replace("{{FILESIZE}}", filesize).replace("{{FILETYPE}}", filetype).replace("{{SERVERHOST}}", str(host)).replace("{{SERVERPOST}}", str(port))

                    page += label

                page += index.split("{{BREAKPOINT}}")[1]
                page = page.encode("utf-8")

                self.response200()
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", len(page))
                self.end_headers()
                self.wfile.write(page)
            except:
                self.response500()

        def do_GET(self):

            path = unquote(self.path)

            print(f"{self.address_string()} GET '{path}'")

            if pwd:
                try:
                    usrpwd = self.headers["pwd"]
                except:
                    usrpwd = ""
                if pwd != usrpwd:
                    self.response403()
                    return

            if path == "/":
                self.sendpage()
                return

            if self.IsAccessible(path):
                self.sendfile(path)
            else:
                self.response403()
                return

        def do_POST(self):

            path = unquote(self.path)

            print(f"{self.address_string()} POST '{path}'")

            self.response403()

    host = gethostbyname_ex(gethostname())[2][-1]
    print(f"Host: {host}, Port: {port}.")
    httpd = ThreadingHTTPServer(("", port), SuperHTTPServer)
    httpd.serve_forever()


if __name__ == '__main__':
    run(port=80, pwd="")
