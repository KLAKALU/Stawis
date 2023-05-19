#ISBN検索
import requests,bs4

def scraping(isbn):
    url=r"https://books.rakuten.co.jp/rb/" + str(isbn) + "/"
    open_=requests.get(url)
    soup_=bs4.BeautifulSoup(open_.content,"html.parser")
    title=soup_.select('#productTitle > h1')
    writer=soup_.select('#productTitle > h1 > a')
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
    if title==[] and writer==[]:
        print("本が見つかりませんでした。")
        return None
    else:
        info = {}
        info["title"] = title[0].getText()
        if writer:
            info["writer"] = writer[0].getText()
        else:
            info["writer"] = None
        info["img_url"] = img_url
        return info

def scraping_(isbn):
    url = r"https://books.rakuten.co.jp/rb/" + str(isbn) + "/"
    open_ = requests.get(url)
    soup_ = bs4.BeautifulSoup(open_.content, "html.parser")
    title = soup_.select('#productTitle > h1')
    writer = soup_.select('#productTitle > h1 > a')
    img = soup_.select('#imageSlider > li.lslide.active > img')
    src = []
    for tag in img:
        src.append(tag.get('src'))
    if src == []:
        print("表紙画像が見つかりませんでした")
    else:
        img_src = src[0]
        img_url = "https://books.rakuten.co.jp" + img_src[2:]
        res = requests.get(img_url, stream=True)
        image_name = img_src.rsplit('/', 1)[1]
        if res.status_code == 200:
            with open(f"images/" + image_name, "wb") as f:
                f.write(res.content)
    if not title and not writer:
        print("本が見つかりませんでした。")
        return None
    else:
        info = {}
        info["title"] = title[0].getText()
        if writer:
            info["writer"] = writer[0].getText()
        else:
            info["writer"] = None
        info["img_url"] = img_url
        return info

