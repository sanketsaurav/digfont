import fix_imports

import webapp2

app = webapp2.WSGIApplication([
								('/', 'views.Home'),
								('/search', 'views.Search'),
								('/populate', 'views.Populate'),
								('/indexer', 'views.Indexer')
							], debug=True)