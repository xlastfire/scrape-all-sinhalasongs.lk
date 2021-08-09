import requests
from bs4 import BeautifulSoup
import os
from time import sleep

main_url = 'https://www.sinhalasongs.lk/sinhala-songs-download/'

def download_song(url,artist_name):

	song_name = url.split('/')[-1]

	song_path = 'songs/' + artist_name + '/' + song_name

	if os.path.isfile(song_path):
		return

	file = requests.get(url)

	with open(song_path,'wb') as f:
		f.write(file.content)

	f.close()

	print('\t ' + song_name + ' downloaded')

def song_direct_link(url,artist_name):

	r = requests.get(url)

	soup = BeautifulSoup(r.content,'html5lib')

	try:
		url = soup.find('div',class_='content_block').a['href']
	except:
		return

	download_song(url, artist_name)



def artist_song_scraper(url):

	artist_name = url.split('/')[-2]

	print('\nScraping ' + artist_name + ' Songs' , end = '')
	
	if not os.path.isdir('songs/' + artist_name):
		os.mkdir('songs/' + artist_name)

	r = requests.get(url)

	soup = BeautifulSoup(r.content,'html5lib')

	song_list = soup.find('ul',class_='page-list subpages-page-list ')

	try:
		songs = song_list.find_all('li')
	
	except:
		print('Nothing Found')
		return

	print(' - Found ' + str(len(songs)) + " songs")

	for song in songs:
		song_direct_link(song.a['href'], artist_name)


def scrape_artists(url):

	r = requests.get(url)

	soup = BeautifulSoup(r.content,'html5lib')


	artist_table = soup.find('ul',class_='page-list subpages-page-list ')

	artists = artist_table.find_all('li')

	print( str(len(artists)) + ' Artists Found! ')
	for artist in artists:
		artist_song_scraper(artist.a['href'])



if __name__ == '__main__':
	if not os.path.isdir('songs'):
		os.mkdir('songs')
	scrape_artists(main_url)