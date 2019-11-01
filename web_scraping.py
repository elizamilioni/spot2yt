import requests
import json
import re
from bs4 import BeautifulSoup
def scan_video(url):
    """Scan the link of the video and return data and."""
    try:
        search_tmplt = "http://www.youtube.com/oembed?url={}&format=json"
        search_url = search_tmplt.format(url)
        r = requests.get(search_url)

        if r.status_code == 200:
            return r.json()
        else:
            return "Unauthorized"

    except Exception:
        return False
def search_yt(querry):
    url = "https://www.youtube.com/results?search_query={}".format(querry)
    response = requests.get(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    count = 0
    video = []
    urls = []
    lim=10
    videos = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})

    for vid in videos:
        if lim == count:
            break
        url = vid['href']
        data = scan_video(url)
        if data == "Unauthorized":
            pass
        elif not data:
            break
        else:
            video.append(data)
            urls.append(url)
            count += 1
    import pdb; pdb.set_trace()
    print(video, urls)
    return (video, urls)

def main():
    contents = requests.get('https://open.spotify.com/playlist/51JDOgdoUznzQlhsO13vmN').content.decode('utf-8')
    html_soup = BeautifulSoup(contents, 'html.parser')
    soup = html_soup.find_all('div', class_="tracklist-col name")
    for i in soup:
        print(i.get_text())
        search_yt(i.get_text())

if __name__ == "__main__":
    main()
