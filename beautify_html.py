from bs4 import BeautifulSoup

raw_html_file = "your_file"
beautiful_html_file = "your_beautiful_file"

with open(raw_html_file, encoding = "utf-8") as html_file, open(beautiful_html_file, 'w', encoding = "utf-8") as outfile:
    htmldocstr = html_file.read()
    doc = BeautifulSoup(htmldocstr, 'html.parser')
    outfile.write(doc.prettify())


