import logging
from flask import Flask, request

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
logfile_handler = logging.FileHandler("server.log")
logger.addHandler(console_handler)
logger.addHandler(logfile_handler)


class HttpServer:
    def __init__(self, **kwargs):
        self.host = kwargs.get("host", "0.0.0.0")
        self.port = kwargs.get("port", 8080)

    @staticmethod
    def server():
        app = Flask(__name__)
        @app.route("/")
        def index():
            return "Index"
        @app.before_request
        def before_request():
            info = "\n------\n{} {}\n".format(request.method, request.full_path)
            for header in request.headers:
                info += "{}: {}\n".format(header[0], header[1])
            info += "\n{}\n".format(request.get_data().decode(errors="ignore"))
            logger.debug(info)
        # @app.after_request
        # def after_request(response):
        #     info ="{}\n".format(response.status)
        #     for header in response.headers:
        #         info += "{}: {}\n".format(header[0], header[1])
        #     info += "\n{}\n------".format(response.get_data().decode(errors="ignore"))
        #     logger.debug(info)
        #     return response
        return app

    def run(self):
        app = self.server()
        app.run(self.host, self.port)


class TCPServer:
    def __init__(self, **kwargs):
        self.host = kwargs.get("host", "0.0.0.0")
        self.port = kwargs.get("port", 8080)

    @staticmethod
    def server():
        pass

    def run(self):
        pass


if __name__ == "__main__":
    http = HttpServer(port=8081)
    http.run()
