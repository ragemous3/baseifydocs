import argparse
import env
from urllib.request import urlopen
from typing import Optional, Any
from bs4 import BeautifulSoup, ResultSet, Tag
import nltk
from fix_text_ai import *

content: Optional[str] = None
rm_elements = set(["meta", "link", "script", "style", "footer", "nav", "aside"])
ignore_elements = set(["hr", "img", "image", "picture", "figcaption", "svg"])


#add keep attribute
keep_attributes = set(["src", "href", "data"])

def main(url: str):
	with urlopen(url) as webpage:
		content = webpage.read().decode()
		cleaned = str(clean_once(content).prettify())
		aifixed = ai_fix(str(cleaned))
		out(content, "raw.html")
		out(cleaned, "index.html")
		out(aifixed, "aifixed.html")
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
	

def clean_once(html: str):
	soup = BeautifulSoup(html, "html.parser") 
 
	for item in soup.find_all(True):
   
		#remove all htlm attr except the ones specified
		if item.attrs:
			item.attrs = {attr: value for attr, value in item.attrs.items() if attr in keep_attributes}
	
		#removes specified elements
		if item.name in rm_elements:
			item.decompose()
			continue
		
	return unwrap(str(soup))


def unwrap(html: str):
	soup = BeautifulSoup(html, "html.parser")
	is_running = False
	for item in soup.find_all(strings=False):
		#Remove elements with no text content
		if item.name not in ignore_elements and not item.get_text(strip=True):
			item.decompose()
			continue

		if item.name not in ignore_elements and item.parent and item.parent.name == item.name and len(list(item.parent.children)) <= 1:
			item.unwrap()
			is_running = True

	return soup if not is_running else unwrap(str(soup))


def out(soup, name):
	with open("output/" + name, "w") as o:
		o.write(str(soup))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="baseifydocs", description="Used for taking snippets of docs and downloading it")
	parser.add_argument("url")
	args = parser.parse_args()
	main(args.url)
