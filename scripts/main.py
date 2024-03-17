import argparse
from urllib.request import urlopen
from typing import Optional, Any
from bs4 import BeautifulSoup, ResultSet

test: str = "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta"

content: Optional[str] = None

rm_elements = set(["meta", "link", "script", "style"])

def main(url: str = test):
	with urlopen(url) as webpage:
		content = webpage.read().decode()
		
		out(clean(content))

def clean(html):
	soup = BeautifulSoup(html, "html.parser")
	item: ResultSet[Any]
	for item in soup.findAll(True):
		#item.attrs = {}
  
		if item.name in rm_elements:
			item.decompose()
			continue

		# If element has no parent and is a div, remove. 
		if not item.parent and item.name == "div":
			item.decompose()
			continue
		
		if len(list(item.contents)) == 0:
			item.decompose()

  		# If the element is div, if the elemet has 1 child and if the that element is a div, remove it.
		if item.name == "div" and len(list(item.contents)) == 1 and list(item.contents)[0].name == "div":
			decoded_contents = item.decode_contents()

			#need to convert back to unicode, include standard set and extra to add ability to remove whatever
			item.insert_after(str(decoded_contents))
			item.decompose()
			continue
   
	return soup

def out(soup):
	with open("output/out.html", "w") as o:
		o.write(soup.prettify())

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="baseifydocs", description="Used for taking snippets of docs and downloading it")
	parser.add_argument("url")
	args = parser.parse_args()
	main(args.url)
