import requests
import argparse
import os
from pathlib import Path
from bs4 import BeautifulSoup
from pytube import YouTube

def main(spotify_url):
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
        path = os.path.join(str(Path.home()), '/Spotify')
        #if not os.path.exists(path):
        #    os.mkdir(path)

        audio[0].download(output_path = os.path.join(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Please give spotify playlist url')
    parser.add_argument('--spotify_url', metavar='S',
                   help='an integer for the accumulator')

    args = parser.parse_args()
    main(args.spotify_url)

