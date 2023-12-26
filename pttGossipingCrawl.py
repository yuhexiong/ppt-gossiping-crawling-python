from bs4 import BeautifulSoup as bs
import requests as req
import json
import os

folderPath = 'data'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)

for page in range(1, 30001):
    url = f"https://www.ptt.cc/bbs/Gossiping/index{page}.html" 
    over18 = {
        "over18": "1"
    }
    res = req.get(url, cookies = over18) 

    soup = bs(res.text, "lxml") 

    link = []
    for l in soup.select('div.r-ent > div.title > a'):
        link.append('https://www.ptt.cc'+l['href']) 

    articles = []
    for subLink in link:
        subRes = req.get(subLink, cookies = over18)
        subSoup = bs(subRes.text, "lxml")
        article = subSoup.select_one("#main-content").get_text()
        content = article.split("※ 發信站:")[0]
        articles.append(content.replace("\n",""))

    with open(f"{folderPath}/ptt{page}.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(articles, ensure_ascii=False))
        print(f"{folderPath}/ptt{page}.json finished!")