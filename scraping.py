import requests
from bs4 import BeautifulSoup
 
url_to_parse = "https://en.wikipedia.org/wiki/Python_(programming_language)"
response = requests.get(url_to_parse)
print(response)
response_text = response.text
soup = BeautifulSoup(response_text, 'lxml')
all_main_headings = []
main_headings = soup.find_all("li", class_="toclevel-1")
for h1 in main_headings:
    heading = h1.find("span", class_="toctext").text
    all_main_headings.append(heading)
    print(heading)