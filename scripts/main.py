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

		content = clean(content, True)
		
		out(content)
		return 1

def clean(html: str, is_running: bool):
	soup = BeautifulSoup(html, "html.parser")
	is_running = False
 
	for item in soup.find_all(True):
		
		#remove all htlm attr except the ones specified
		if item.attrs:
			item.attrs = {attr: value for attr, value in item.attrs.items() if attr in keep_attributes}
  
		if item.name in rm_elements:
			is_running = True
			item.decompose()
			continue

		# Bug, strip=True trim whitespaces, 
		if not item.get_text(strip=True):
			is_running = True
			item.decompose()
			continue

  		# If the element is div, if the elemet has 1 child and if the that element is a div, remove it.
		if item.name == item.parent.name and len(list(item.contents)) == 1:
			for kid in item.children:
				item.insert_after(kid)
			item.decompose()
			is_running = True
			continue
	
	if is_running:
		clean(str(soup), is_running)
   
	return soup.prettify()

def out(soup):
	with open("output/out.html", "w") as o:
		o.write(str(soup))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="baseifydocs", description="Used for taking snippets of docs and downloading it")
	parser.add_argument("url")
	args = parser.parse_args()
	main(args.url)

""" 		if not item.parent and item.name == "div":
			item.decompose()
			continue """