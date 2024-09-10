import argparse
from typing import Optional
from urllib.request import urlopen
import env
from scripts.services.gpt_style import document_style
from services.gpt_service import *
from modules.html_parser import add_style_sheet, clean

content: Optional[str] = None

def main(url: str, clean_html: bool, memorize: bool, model: str, style: bool) -> int:
	with urlopen(url) as webpage:
		content = webpage.read().decode()
		result = content
  
		if clean_html:
			result = clean(content)

		aifixed = gpt_service(str(result), model, memorize)

		if style:
			style_tag = document_style()
			aifixed = add_style_sheet(aifixed, style_tag)
			
  
		out(result, "raw.html")
		out(result, "index.html")
		out(aifixed, "aifixed.html")
		return 1

def out(soup, name):
	with open("output/" + name, "w") as o:
		o.write(str(soup))


# python3 main.py --url=https://docs.docker.com/guides/walkthroughs/what-is-a-container/ --clean_html=true
if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="baseifydocs", description="Used for taking snippets of docs and downloading it")
 
	parser.add_argument("--clean_html", type=bool, default=True, help="Cleans the html. Default is true.")
	parser.add_argument("--url", type=str, help="URL of the webpage you want to process")
	parser.add_argument("--model", type=str, default="gpt-4o")
	parser.add_argument("--memorize", type=bool, help="Make gpt memorize")
	parser.add_argument("--style", type=bool, help="Style the html")

 
	args = parser.parse_args()
 
	main(args.url, args.clean_html, args.memorize, args.model)
