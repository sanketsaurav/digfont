from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class Font(ndb.Model):
	"""
	Font data.
	"""

	name = ndb.StringProperty(indexed=True)
	site_url = ndb.StringProperty(required=True, indexed=True)
	created = ndb.DateTimeProperty(auto_now_add=True)
	updated = ndb.DateTimeProperty(auto_now=True)