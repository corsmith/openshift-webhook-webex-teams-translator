import tornado.ioloop
import tornado.web

async def f():
    http_client = AsyncHTTPClient()
    try:
        response = await http_client.fetch("http://www.google.com")
    except Exception as e:
        print("Error: %s" % e)
    else:
        print(response.body)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
