import webapp2

from google.appengine.api import search

from config import *
from utils import * 
from models import Font

class BaseHandler(webapp2.RequestHandler):
	"""
	Base class for view functions, which provides basic rendering 
	funtionalities
	"""

	def render(self, template, **kw):
		"""
		Render a template with the given keyword arguments
		"""

		self.response.out.write(render_str(template, **kw))

	def set_secure_cookie(self, name, val):
		"""
		Set an encrypted cookie on client's machine
		"""

		cookie_val = make_secure_val(val)
		self.response.headers.add_header(
			'Set-Cookie',
			'%s=%s; Path=/' % (name, cookie_val)
			)

	def read_secure_cookie(self, name):
		"""
		Read a cookie and check it's integrity
		"""

		cookie_val = self.request.cookies.get(name)
		return cookie_val and check_secure_val(cookie_val)

	def initialize(self, *a, **kw):
		"""
		Override the constuctor for adding user information
		when a request comes
		"""

		webapp2.RequestHandler.initialize(self, *a, **kw)
		user_id = self.read_secure_cookie('user')
		self.user = user_id and User.get_by_id(int(user_id))

class Home(BaseHandler):
	"""
	Render the homepage.
	"""

	def get(self):
		"""
		For a GET request, render the homepage.
		"""

		self.render("home.html")

class Search(BaseHandler):

	def get(self):
		
		query = self.request.get("q")

		if query:
			try:
				index = search.Index('fontindex')
				results = index.search(query)

				total_matches = results.number_found
				result_list = results.results

				font_results = [{'fonts' : result.fields[0].value, 'url' : result.fields[1].value} for result in result_list]


				self.render("results.html", results=font_results, query=query, number=total_matches)


			except:
				return 'Error!'

class Populate(BaseHandler):
	"""
	Populates the database.
	"""

	def post(self):
		start = self.request.get("start")
		end = self.request.get("end")

		index = search.Index(name='fontindex')
		with open('seed.txt', 'r') as f:
			urls = f.read().split('\n')[int(start):int(end)]

		for url in urls:
			try:
				fonts = get_all_fonts(url)
				if fonts:
					f = Font(name=fonts, site_url=url)
					f_key = f.put()

					if f_key:
						font_doc = search.Document(
							fields=[
								search.TextField(name='name', value=fonts),
								search.TextField(name='site_url', value=url)
						])

						index.put(font_doc)

			except: pass

		self.response.out.write('Done!')

class Indexer(BaseHandler):
	"""
	Indexes the datastore.
	"""

	def put(self):

		index = search.Index(name='fontindex')
		fonts = Font.query()


		for font in fonts:
			font_doc = search.Document(
				fields=[
					search.TextField(name='name', value=font.name),
					search.TextField(name='site_url', value=font.site_url)
			])

			index.put(font_doc)

		self.response.out.write('Done!')