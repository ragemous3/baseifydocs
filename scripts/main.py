import argparse
import env
from urllib.request import urlopen
from typing import Optional, Any
from bs4 import BeautifulSoup, ResultSet
from fix_text_ai import *

content: Optional[str] = None

rm_elements = set(["meta", "link", "script", "style", "footer", "nav", "svg", "aside", "button"])

#add keep attribute
keep_attributes = set(["", ""])

def main(url: str):
	with urlopen(url) as webpage:
		content = webpage.read().decode()
  		#use ai outside of the context  . After the cleaninzzg has been done. Instruct to be non-recursive. 
		#Figure out how to only get relevan strings. 
  
		content = clean(content)
		# clean_text(content)
		out(content.prettify(), "out.html")
		return 1

def clean_text(soup: BeautifulSoup):
    
    for item in soup.find_all(True):
        print("made print")
        print(item.get_text())
    

def clean(html: str, is_running: bool = False):
	soup = BeautifulSoup(html, "html.parser") 
 
	for item in soup.find_all(True):
   
		#remove all htlm attr except the ones specified
		if item.attrs:
			item.attrs = {attr: value for attr, value in item.attrs.items() if attr in keep_attributes}
	
		#removes specified elements
		if item.name in rm_elements:
			is_running = True
			item.decompose()
			continue

		#Remove elements with no text content
		if not item.get_text(strip=True):
			is_running = True
			item.decompose()
			continue
		
		#Erases unecessary stacked containers
		if item.name == item.parent.name and len(list(item.contents)) == 1:
			for kid in item.children:
				item.insert_after(kid)
			item.decompose()
			is_running = True
			continue
   
	return soup if not is_running else clean(str(soup))

def out(soup, name):
	with open("output/" + name, "w") as o:
		o.write(str(soup))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="baseifydocs", description="Used for taking snippets of docs and downloading it")
	parser.add_argument("url")
	args = parser.parse_args()
	main(args.url)
