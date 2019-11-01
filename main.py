import requests
import os
from bs4 import BeautifulSoup
from pytube import YouTube



def main(spotify_url,saving_dir):
    ret = requests.get(spotify_url)
    retcon = ret.content.decode('utf-8')
    file = open(os.path.join(os.getcwd(), 'spotify.html'),'w')
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


        audio[0].download(output_path = saving_dir)

if __name__ == "__main__":
    spotify_url = input('Give me spotify url: ')
    saving_dir = input('Give me the path of the folder to save the songs: ')
    main(spotify_url,saving_dir)

    files = os.listdir(saving_dir)

    for i in files:
        if 'mp4' in str(i):
            name, _ = i.split('.')
            os.rename(saving_dir + '/' + i, saving_dir + '/' + name + '.mp3')