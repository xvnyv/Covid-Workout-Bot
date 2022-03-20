import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

driver = webdriver.Chrome(os.getenv("DRIVER_PATH"))

class ChloeTingChallenge:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.days = 0
        self.schedule = {}  # for day 1, it will be 1: [vid1 link, vid2 link, vid3 link]

    def setSchedule(self):
        driver.get(self.link)
        challenge_soup = BeautifulSoup(driver.page_source, 'html.parser')
        calendar = challenge_soup.find_all('div', class_='cal-entry')
        self.days = len(calendar)
        for (index, day) in enumerate(calendar):
            videos = day.find_all('a')
            video_links = []
            for video in videos:
                title = str(video.find('p')).lstrip('<p>').rstrip('</p>').lstrip().rstrip()
                video_link = str(video).split('"')[1]
                mandatory = video.find('div', class_='optional') == None
                if mandatory:
                    video_links.append(f'{video_link}|{title.replace("&amp;", "and")}')
                else:
                    video_links.append(f'*{video_link}|{title.replace("&amp;", "and")}')
            self.schedule[index+1] = video_links 

URL = 'https://www.chloeting.com/program/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
titles = [str(title).lstrip('<p class="title">').rstrip('</p>') for title in soup.findAll('p', class_='title')]
links = [str(link).split('>')[0].split('"')[1] for link in soup.find_all('a', href=True)]
challenge_links = list(filter(lambda x: x[:2] == '20', links))
challenges = [ChloeTingChallenge(title.replace('&amp;', 'and'), URL+link) for (title, link) in zip(titles, challenge_links)]
challenges.pop()   # format of the last challenge's page is different from the rest

f = open('../workout_files/chloe_ting_challenges.txt', 'w')

for (index, challenge) in enumerate(challenges):
    challenge.setSchedule()
    f.write(f'T>{challenge.title.replace("&amp;", "and")}\n')
    for day in range(1, challenge.days+1):
        f.write(f'{day}>{",".join(challenge.schedule[day])}\n')

f.close()
print('file has been updated')

