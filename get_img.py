import requests
import os

with open('meme_links.txt', 'r') as f:
	memes_str = f.read()

memes_list = memes_str.split('\n')
num_memes = len(memes_list)
test_link = memes_list[0]

print(test_link)

for i in range(100):
	os.makedirs(f'/Volumes/A041/memes/{i:02d}')

print('Created subdirectories')

def download_image(img_url, file_name):
	try:
		full_img = requests.get(img_url, stream=True)
		full_img.raise_for_status()
		subdir = str(hash(file_name))[-2:]

		with open(f'/Volumes/A041/memes/{subdir}/{file_name}', 'wb') as img_file:
			for chunk in full_img.iter_content(chunk_size=8192):
				img_file.write(chunk)

	except requests.exceptions.RequestException as e:
		print(f'Error downloading iamge: {e}')


for i in range(len(memes_list)):
	try:
		img_name = memes_list[i].split('/')[-1]
		download_image(memes_list[i], img_name)
		
		if i % 50 == 0:
			print(f'Downloaded {i} / {num_memes}')
	except Exception as e:
		print(f'error downloading {memes_list[i]}: {e}')
