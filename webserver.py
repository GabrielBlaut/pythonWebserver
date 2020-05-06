
from http.server import HTTPServer,BaseHTTPRequestHandler

class myRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<html><body>")
                self.wfile.write(b"<b>Hallo</b>")
                self.wfile.write(b"</html></body>")
            else:
                self.send_error(404,"File not Found %s" % self.path)

        except IOError :
            self.send_error(404) 


def main():
    try:
        port=8000
        myServer=HTTPServer(('',port),myRequestHandler)
        print ("webserver running on %s" % port)
        myServer.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()

if __name__ == "__main__":
    main()