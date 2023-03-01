import shutil,requests,bs4,codecs
def scraping(isbn):
    url=r"https://www.kinokuniya.co.jp/f/dsg-01-" + str(isbn)
    open_=requests.get(url)
    soup_=bs4.BeautifulSoup(open_.content,"html.parser")
    title=soup_.select('h3[itemprop="name"]')
    writer=soup_.select('div[class="infobox ml10 mt10"] > ul > li')
    com=soup_.select('div[class="infobox ml10 mt10"] > ul > li > a')
    price=soup_.select('div[class="infobox ml10 mt10"] > ul > li')
    soup_img = bs4.BeautifulSoup(requests.get(url).content, 'lxml')
    src=[]
    for link in soup_img.find_all('img'):
        if link.get('src').endswith('.jpg'):
            src.append(link.get('src'))
    if src==[]:
        print("表紙画像が見つかりませんでした")
    else:
        img_src=src[1]
        img_url="https://www.kinokuniya.co.jp" + img_src[2:]
        res = requests.get(img_url, stream=True)
        if res.status_code == 200:
            img=open("./static/img/im.jpg", 'wb')
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, img)
    if title==[] and writer==[] and com==[] and price==[]:
        return "本が見つかりませんでした。"
    else:
        title_=title[0].getText()
        writer_=writer[0].getText()
        com_=com[1].getText()
        price_=price[2].getText()
        info=[title_, writer_, com_, price_, url]
    ***REMOVED***
