import requests
from bs4 import BeautifulSoup
import time
from rich import print
def search_dramas(query):
    url = f"https://asianc.to/search?type=movies&keyword={query}&sort=views"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    dramas = []
    drama_elements = soup.find_all("li")

    for drama_elem in drama_elements:
        h3_elem = drama_elem.find("h3", class_="title")
        if h3_elem:
            drama_name = h3_elem.text.strip()
            drama_url = drama_elem.find("a")["href"]
            image_url = drama_elem.find("img")["src"]
            dramas.append({
                "name": drama_name,
                "url": drama_url,
                "image_url": image_url
            })

    return dramas
# print(search_dramas("queen of"))
# Ensure this function is in your crawler.py or wherever your scraping logic is
def drama_episodes(drama_url):
    response = requests.get(drama_url)
    soup = BeautifulSoup(response.content, "html.parser")

    episodes = []
    episodes_elem = soup.find_all("li")
    for episode_elem in episodes_elem:
        h3_elem = episode_elem.find("h3", class_="title")
        if h3_elem:
            episode_name = h3_elem.text.strip()
            episode_url = episode_elem.find("a")["href"]
            episodes.append({"name": episode_name, "url": episode_url})

    return episodes

def download_btn(episode_url):
    response = requests.get(episode_url)
    soup = BeautifulSoup(response.content, "html.parser")
    quality_elem = soup.find("li", class_="download")
    if quality_elem:
        download_btn = quality_elem.find("a")["href"]
        if not download_btn.startswith('http'):
          download_btn = 'https:' + download_btn
          return download_btn
    else:
        return None
# print(download_btn("https://dramacool.bg/video-watch/queen-of-tears-2024-episode-9"))

#print(download_btn("https://dramacool.bg/video-watch/queen-of-tears-2024-episode-9"))
# def download_link(download_btn):
#     # Add the scheme to the URL if missing
#     if not download_btn.startswith('http'):
#         download_btn = 'https:' + download_btn
#     print(download_btn)
#     response = requests.get(download_btn)
#     time.sleep(3)
#     soup = BeautifulSoup(response.content, "html.parser")
#     quality_elems = soup.find_all("div", class_="dowload")  # Note the class name might have a typo, adjust as necessary
#     print(quality_elems)
#     links = []
#     for quality_elem in quality_elems:
#         download_link = quality_elem.find("a")["href"]
#         quality_text = quality_elem.text.strip()
#         links.append({"quality": quality_text, "url": download_link})
#     return links
# # print(download_link("https://pladrac.net/download?id=NDA2NjA0&typesub=dramacool-SUB&title=Queen+of+Tears+%282024%29+episode+9"))

