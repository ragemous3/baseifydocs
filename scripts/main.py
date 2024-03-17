import argparse
from urllib.request import urlopen
from typing import Optional, Any
from bs4 import BeautifulSoup, ResultSet

test: str = "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta"

content: Optional[str] = None

rm_elements = set(["meta", "link", "script", "style", "footer", "nav", "svg", "aside", "button"])

#add keep attribute
keep_attributes = set(["href", "src"])

def main(url: str = test):
	with urlopen(url) as webpage:
		content = webpage.read().decode()

		for i in range(0, 3):
			content = clean(content)

		out(content)
		return 1

#Not recursive, content will have empty divs etc after this is done. No good.

def clean(html):
	soup = BeautifulSoup(html, "html.parser")
	item: ResultSet[Any]
	for item in soup.findAll(True):
     
		#remove all htlm attr
		item.attrs = {}
  
		if item.name in rm_elements:
			item.decompose()
			continue

		# Bug, it removes too much
		if not item.findAll(True):
			item.decompose()
			continue

		if not item.get_text():
			item.decompose()
			continue

  		# If the element is div, if the elemet has 1 child and if the that element is a div, remove it.
		if item.name == "div" and len(list(item.contents)) == 1 and list(item.contents)[0].name == "div":
			for kid in item.children:
				item.insert_after(kid)
			item.decompose()
			continue
   
	return soup.prettify()

def out(soup):
	with open("output/out.html", "w") as o:
		o.write(soup)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="baseifydocs", description="Used for taking snippets of docs and downloading it")
	parser.add_argument("url")
	args = parser.parse_args()
	main(args.url)

""" 		if not item.parent and item.name == "div":
			item.decompose()
			continue """