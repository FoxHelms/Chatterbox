import requests
from bs4 import BeautifulSoup
import re

# Dynamically get page count
base_url = 'https://knowyourmeme.com/memes/page/'
home_pg_resp = requests.get('https://knowyourmeme.com/memes')
home_soup = BeautifulSoup(home_pg_resp.content, 'html.parser')

page_buttons = [re.sub(r'[^0-9]','',butt.get_text()) for butt in home_soup.find_all('a', 
attrs={'class':'page-button'})]
butt_nums = [int(butt) for butt in page_buttons if butt]
last_page = max(butt_nums)
all_links = []

for i in range(1, last_page + 1):
	response = requests.get(base_url + str(i))
	soup = BeautifulSoup(response.content, 'html.parser')
	meme_links = []

	imgs = soup.find_all('img')
	for img in imgs:
		if img.get('data-image'):
			meme_links.append(img.get('data-image'))

	print(f'Page {i} of {last_page}')

	if i % 100 == 0:
		print(f'Batch from page {i}')
		print('\n'.join(meme_links))

	with open('meme_links.txt', 'a') as file:
		file.write('\n'.join(meme_links))