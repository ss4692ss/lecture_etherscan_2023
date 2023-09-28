import pandas
import os

from bs4 import BeautifulSoup

if not os.path.exists("parsed_files"):
	os.mkdir("parsed_files")

file_name = "html_files/20230928155418.html"

file = open(file_name, "r")

soup = BeautifulSoup(file.read(), 'html.parser')

file.close()


