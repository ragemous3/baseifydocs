import argparse
import env
from urllib.request import urlopen
from typing import Optional, Any
from bs4 import BeautifulSoup, ResultSet, Tag
import nltk
from fix_text_ai import *

content: Optional[str] = None
rm_elements = set(["meta", "link", "script", "style", "footer", "nav", "aside"])
ignore_elements = set(["hr", "img", "image", "picture", "figcaption", "svg", "button"])


#add keep attribute
keep_attributes = set(["src", "href", "data"])

def main(url: str):
	with urlopen(url) as webpage:
		content = webpage.read().decode()
		content = str(clean(content).prettify())
		aifixed = ai_fix(str(content))
		out(content, "raw.html")
		out(aifixed, "index.html")
		return 1

def ai_fix(text, chunk_size=1000):
	sentences = nltk.sent_tokenize(text)
	chunks = []
	current_chunk = ""
	
	for sentence in sentences:
		if len(current_chunk) + len(sentence) <= chunk_size:
			current_chunk += sentence
		else:
			chunks.append(current_chunk)
			current_chunk = sentence
	
	if current_chunk:
		chunks.append(current_chunk)
	
	ai_fixed: str = ""
	for i, chunk in enumerate(chunks):
		ai_fixed += make_better(chunk)
	return ai_fixed
	

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
		if item.name not in ignore_elements and not item.get_text(strip=True):
			is_running = True
			item.decompose()
			continue
		
		#Erases unecessary stacked containers
		if item and item.parent and isinstance(item, Tag) and item.name == item.parent.name and len(list(item.contents)) == 1:
			item.unwrap()
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
