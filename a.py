import requests,json,os

isbn = "9784309226712"

apikey = os.getenv('WEBAPI_KEY')


def getbookdetails(isbn):
    baserequest = 'https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404'
    appid = '?applicationId=' + apikey
    value = '&isbnjan=' + isbn
    uri = baserequest + appid + value
    r = requests.get(uri)
    json_load = r.json()
    print(json.dumps(json_load, indent=2, ensure_ascii=False))
    info = {}
    info["title"] = json_load['Items'][0]['Item']['title']
    info['writer'] = json_load['Items'][0]['Item']['author']
    return info

info = getbookdetails(isbn)

print(info['title'])

print(info['writer'])
apikey = 1013588615548646752