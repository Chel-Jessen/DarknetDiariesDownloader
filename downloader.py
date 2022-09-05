import requests
import bs4
import json

URL = "https://darknetdiaries.com/episode/"
IMAGE_URL = "https://darknetdiaries.com/imgs"


class Episode:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.number = None
        self.thumbnail_url = None
        self.length = None
        self.download_link = None
        self.upload_date = None
        self.tags = None
        self.get_episode_details()

    
    def get_episode_details(self):
        resp = requests.get(self.url)
        if resp.status_code != 200:
            raise Exception
        soup = bs4.BeautifulSoup(resp.text,'html.parser')
        for script in soup.find_all("script"):
                if "src" not in str(script):
                    info_str = "".join(str(script).split("=")[1:]).split("<")[0]
                    info = json.loads(info_str)["episode"]
        self.title = info["title"].replace(":", " ")
        self.number = self.url.split("/")[-2]
        self.thumbnail_url = soup.find("img").extract()["src"]
        self.length = info["subtitle"]
        self.download_link = info["media"]["mp3"]
        self.upload_date = str(soup.find("p")).split(" |")[0].split(">")[-1]
        try:
            for a in soup.find_all("a"):
                if "div" in str(a.contents):
                    self.tags = [str(tag).split(">")[1].split("<")[0] for tag in a]
        except:
            pass

    def download_episode(self):
        resp = requests.get(self.download_link)
        with open(f"./Episodes/{self.title} - Darknet Diaries.mp3", "wb") as file:
            file.write(resp.content)


def get_latest_episode():
    episode = 1
    while True:
        resp = requests.get(f"{URL}{episode}")
        if resp.status_code != 200:
            return episode - 1
        episode += 1

def download_all_episodes(latest_episode:int=0, start_episode:int=1):
    if latest_episode == 0:
        latest_episode = get_latest_episode()
    for episode_number in range(start_episode, latest_episode + 1):
        episode = Episode(f"{URL}{episode_number}")
        episode.download_episode()
        print(episode_number)
