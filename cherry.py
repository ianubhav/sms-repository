import cherrypy
from jinja2 import Environment, FileSystemLoader
import urllib.request as urllib2,json
import os
import utils
from datetime import datetime,timedelta
import json
from json.decoder import JSONDecodeError

env = Environment(loader=FileSystemLoader('templates'))

PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')

class Root:
	@cherrypy.expose
	def index(self):
		tmpl = env.get_template('index.html')
		return tmpl.render()

	@cherrypy.expose
	@cherrypy.tools.json_out()
	def upload(self, json_file):
		cwd = os.getcwd()
		upload_file = os.path.join(cwd,'files', json_file.filename)

		with open(upload_file, 'wb') as out:
			file_contents = json_file.file.read()
			out.write(file_contents)
		try:
			msg_dict = json.loads(file_contents.decode())
			msgs = utils.parse_json_msg(msg_dict['messages'])
			return msgs
		except JSONDecodeError as e:
			return []


config = {
	'/static':{
	'tools.staticdir.on': True,
	'tools.staticdir.dir': PATH
	}
}

cherrypy.tree.mount(Root(), '/', config = config)
cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.config.update({'server.socket_port': 9000})
cherrypy.engine.start()

