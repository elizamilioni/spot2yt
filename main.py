from bs4 import BeautifulSoup
import requests
from pytube import YouTube

spotify_url = 'https://open.spotify.com/playlist/1syrBGr8ecpmTABM6ntyLK'
ret = requests.get(spotify_url)
retcon = ret.content.decode('utf-8')
file = open('/home/nikopi/Desktop/spotify.html','w').close()
file = open('/home/nikopi/Desktop/spotify.html','w')
file.write(retcon)
file.close()

html_soup = BeautifulSoup(retcon, 'html.parser')
conts = html_soup.find_all('div', class_ = 'tracklist-col name')
tracks = []
for i in conts:
    trackname = i.find('span', class_ = 'track-name')
    trackname.append(' ')
    artists = i.find_all('a',href = True)
    for j in artists:
        trackname.append(j.text+ ' ')
        break
    tracks.append(trackname.text + ' ')

for i in tracks:

    t = i.replace('(', '')
    t = t.replace(')', '')
    t = t.replace("'", '')
    t = t.replace(' ', '+')
    t = t.replace('"', '')
    t = t.replace('’','')
    you_url = 'https://www.youtube.com/results?search_query=' + t[:-2]

    ret = requests.get(you_url).content.decode('utf-8')
    html_soup = BeautifulSoup(ret, 'html.parser')
    vid =  html_soup.findAll(attrs={'class': 'yt-uix-tile-link'})
    song_url = 'https://www.youtube.com' + vid[0]['href']
    print(song_url)
    yt = YouTube(song_url)
    audio = yt.streams.filter(only_audio = True).all()
    audio[0].download(output_path = '/home/nikopi/Desktop/Spotify')

