from urllib.request import urlopen;
from typing import Optional;
from bs4 import BeautifulSoup;
url: str = "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta";

content: Optional[str] = None;

with urlopen(url) as webpage:
	content = webpage.read().decode();

if content:
	with open("output/out.html", "w") as out:
		soup = BeautifulSoup(content, "html.parser");
		out.write(soup.prettify());
