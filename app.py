import tornado.ioloop
import tornado.web
import tornado.options 
from tornado.log import gen_log

'''
Alert Manager Documentation: https://prometheus.io/docs/alerting/configuration/

Sample alertmanager message:

{
  "version": "4",
  "groupKey": <string>,    // key identifying the group of alerts (e.g. to deduplicate)
  "status": "<resolved|firing>",
  "receiver": <string>,
  "groupLabels": <object>,
  "commonLabels": <object>,
  "commonAnnotations": <object>,
  "externalURL": <string>,  // backlink to the Alertmanager.
  "alerts": [
    {
      "status": "<resolved|firing>",
      "labels": <object>,
      "annotations": <object>,
      "startsAt": "<rfc3339>",
      "endsAt": "<rfc3339>",
      "generatorURL": <string> // identifies the entity that caused the alert
    },
    ...
  ]
}
'''

async def f():
    http_client = AsyncHTTPClient()
    try:
        response = await http_client.fetch("http://www.google.com")
    except Exception as e:
        print("Error: %s" % e)
    else:
        print(response.body)

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world\n")

class MainHandler(tornado.web.RequestHandler):
    def post(self, webhookkey):
        gen_log.warning(f'webhookkey = { webhookkey }\nuri: { self.request.uri }\nquery: { self.request.query }\nheaders: { self.request.headers }\nbody: { self.request.body }')
        self.write("Hello, %s\n" % webhookkey)

def make_app():
    return tornado.web.Application([
        (r"/v1/webhooks/incoming/([^/]+)", MainHandler),
        (r"/", HealthHandler),
    ])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
