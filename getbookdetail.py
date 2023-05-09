import requests
import json


def getbookdetail(apikey,isbn):
    endpoint = 'https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404'
    appid = '?applicationId=' + apikey
    value = '&isbnjan=' + isbn
    uri = endpoint + appid + value
    r = requests.get(uri)
    json_load = r.json()
    print(json.dumps(json_load, indent=2, ensure_ascii=False))
    info = {}
    info["title"] = json_load['Items'][0]['Item']['title']
    info['writer'] = json_load['Items'][0]['Item']['author']
    return info