import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from urls import urlList
from utils.logger_setup import logger

define("port", default=8090, help="run on the given port", type=int)

class EducationPortal(tornado.web.Application):

    def __init__(self):
        handlers = urlList
        settings = dict(
            debug=True,
            cookie_secret="61oETz3455545gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            autoescape=None,  # Disable autoescaping to prevent template path issues
            compiled_template_cache=False,  # Disable template caching for development
            serve_traceback=True,  # Enable detailed tracebacks for debugging
            template_whitespace="all",  # Preserve whitespace to avoid path resolution issues


        )
        tornado.web.Application.__init__(self,handlers,**settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    logger.info("Starting Tornado EducationPortal on port {}", options.port)
    try:
        http_server = tornado.httpserver.HTTPServer(EducationPortal())
        http_server.listen(options.port)
        # Use current() in Tornado 6+ for the running loop
        tornado.ioloop.IOLoop.current().start()
    except Exception:
        logger.exception("Uncaught exception while running server")
        raise