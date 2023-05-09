#ISBN検索
import requests,bs4

def scraping(isbn):
    url=r"https://books.rakuten.co.jp/rb/" + str(isbn) + "/"
    open_=requests.get(url)
    soup_=bs4.BeautifulSoup(open_.content,"html.parser")
    title=soup_.select('#productTitle > h1')
    writer=soup_.select('#productTitle > h1 > a')
    #com=soup_.select('div[class="infobox ml10 mt10"] > ul > li > a')
    #price=soup_.select('div[class="infobox ml10 mt10"] > ul > li')
    # soup_img = bs4.BeautifulSoup(requests.get(url).content, 'lxml')
    img = soup_.select('#imageSlider > li.lslide.active > img')
    print(img)
    src=[]
    for link in img.find('img'):
        if link.get('src').endswith('.jpg'):
            src.append(link.get('src'))
    if src==[]:
        print("表紙画像が見つかりませんでした")
    else:
        img_src=src[1]
        img_url="https://www.kinokuniya.co.jp" + img_src[2:]
        res = requests.get(img_url, stream=True)
        image_name = img_src[2:].rsplit('/', 1)[1]
        if res.status_code == 200:
            with open(f"images/" + image_name, "wb") as f:
                f.write(res.content)
            # img=open("./static/img/im.jpg", 'wb')
            # res.raw.decode_content = True
            # shutil.copyfileobj(res.raw, img)
    if title==[] and rawwriter==[]:
        print("本が見つかりませんでした。")
        return None
    else:
        info = {}
        info["title"] = title[0].getText()
        if writer:
            info["writer"] = writer[0].getText()
        else:
            info["writer"] = null
        #info["com"] = com[1].getText()
        #info["price"] = price[2].getText()
        info["img_url"] = img_url
        return info
