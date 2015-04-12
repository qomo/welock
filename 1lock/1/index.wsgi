import os
import tornado.wsgi

import sae

from onelock import urls as mainurls

#class MainHandler(tornado.web.RequestHandler):
#    def get(self):
#        self.write("Hello, world! - Tornado")


settings = {
	'debug': True,
	'template_path': os.path.join(os.path.dirname(__file__), "templates"),
}

app = tornado.wsgi.WSGIApplication(mainurls, **settings)

application = sae.create_wsgi_app(app)