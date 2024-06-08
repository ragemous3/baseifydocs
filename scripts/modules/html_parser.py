from bs4 import BeautifulSoup
import htmlmin

rm_elements = set(["meta", "link", "script", "style", "footer", "nav", "aside"])
ignore_elements = set(["hr", "img", "image", "picture", "figcaption", "svg"])
keep_attributes = set(["src", "href", "data"])

def clean(
	html: str) -> str:
	soup = BeautifulSoup(html, "html.parser") 
 
	for item in soup.find_all(True):
	 
		if item.name in ignore_elements:
			continue
   
		if item.attrs:
			item.attrs = {attr: value for attr, value in item.attrs.items() if attr in keep_attributes}
	
		if item.name in rm_elements:
			item.decompose()
			continue
		
	return  htmlmin.minify(str(unwrap(soup)), remove_empty_space=True)


def unwrap(soup: BeautifulSoup) -> BeautifulSoup:
	is_running = False
	for item in soup.find_all(strings=False):
		
		if item.name in ignore_elements:
			continue
		
		if not item.get_text(strip=True):
			item.decompose()
			continue

		if item.parent and item.parent.name == item.name and len(list(item.parent.children)) <= 1:
			item.unwrap()	
			is_running = True

	return soup if not is_running else unwrap(soup)