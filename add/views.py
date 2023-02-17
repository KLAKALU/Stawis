from flask import request,render_template
from add.init import app
@app.route("/")
def show_():
    return render_template("b.html")

import requests,bs4,codecs
@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        isbn=str(request.form['ISBN'])
        url=r"https://www.kinokuniya.co.jp/f/dsg-01-" + isbn
        open_=requests.get(url)
        soup_=bs4.BeautifulSoup(open_.content,"html.parser")
        #タイトル
        title=soup_.select('h3[itemprop="name"]')
        title_=title[0].getText()
        print("タイトル:" + title_)
        #著書名
        writer=soup_.select('div[class="infobox ml10 mt10"] > ul > li')
        writer_=writer[0].getText()
        print("著書名："+ writer_)
        #出版社
        com=soup_.select('div[class="infobox ml10 mt10"] > ul > li > a')
        com_=com[1].getText()
        print("出版社："+ com_)
        #値段
        price=soup_.select('div[class="infobox ml10 mt10"] > ul > li')
        price_=price[2].getText()
        print(price_)
        #表紙画像
        soup_img = bs4.BeautifulSoup(requests.get(url).content, 'lxml')
        src=[]
        for link in soup_img.find_all('img'):
            if link.get('src').endswith('.jpg'):
                src.append(link.get('src'))
        img_src=src[1]
        img_url="https://www.kinokuniya.co.jp" + img_src[2:]
        print(img_url)

        file = codecs.open("./add/templates/a.html",'w','utf-8','ignore')
        s = '\xa0'
        file.write(s)
        file.write("<meta charset='utf-8'>")
        file.write("<div>" + title_ + "</div>\n<div>" + writer_ + "</div>\n<div>" + com_ + "</div>\n<div>" + price_ + "</div>")
        file.write('<a href="' + url + '">購入はこちら</a>\n')
        file.write('<img src="' + img_url + '">')
        file.close()

        return render_template('a.html')