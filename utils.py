from BeautifulSoup import BeautifulSoup
import tinycss
import requests

from config import *

def render_str(template, **params):
	"""
	Return a string rendered by a Jinja2 template
	"""

	t = JINJA_ENV.get_template(template)
	return t.render(params)

def convert_relative_url(url, site_url):
	chopped_url = site_url.split("//")
	if url.startswith('//'):
		scheme = chopped_url[0]
		return scheme + url
	elif url.startswith("http"):
		return url
	else:
		return site_url + url

def fetch_css(url, site):
	url = convert_relative_url(url, site)
	resp  = requests.get(url)
	return resp.content

def fetch_css_links(site):
	"""
	Fetches all CSS links on the given URL. Returns a BeautifulSoup ResultSet.
	"""

	resp = requests.get(site)
	if resp.ok:
		soup = BeautifulSoup(resp.content)
		return soup.findAll('link', rel='stylesheet')
	raise Exception(u"Unable to process because of status code: {0}".format(resp.status_code))

def fetch_fonts(css):
	"""
	Returns a LIST of all fonts in the CSS
	"""
	
        parser = tinycss.make_parser('page3')
        stylesheet = parser.parse_stylesheet(css)
        
	fonts = []
	for rule in stylesheet.rules:
            try:
                declarations = rule.declarations
                
                for declaration in declarations:
                    if declaration.name == 'font-family':
                        #print declaration.value
                        fstring = ' '.join([token.value for token in declaration.value])
                        fonts.append(fstring)
            except: pass
        return fonts
    
def clean_fonts(fonts):
	EXCLUDE = ('sans-serif', 'serif', 'inherit', 'monospace', '!important', '"', "'", ',')
	for rule in EXCLUDE:
		if rule in fonts:
			fonts = fonts.replace(rule, ' ')
	return fonts
    
def get_all_fonts(site):
	"""
	Fetches all fonts on a website, returns a string of font names
	"""

	# Fetch all CSS files found on the website
	css_urls = fetch_css_links(site)
        
	for url in css_urls:
		css = fetch_css(url['href'], site)
                fonts = clean_fonts(' '.join(fetch_fonts(css)))
                return ' '.join(set(fonts.strip().split('  '))).strip().lower()

