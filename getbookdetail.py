import requests


def getbookdetail(apikey,isbn):
    endpoint = 'https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404'
    appid = '?applicationId=' + apikey
    value = '&isbnjan=' + isbn
    uri = endpoint + appid + value
    r = requests.get(uri)
    json_load = r.json()
    info = {}
    info["title"] = json_load['Items'][0]['Item']['title']
    info['writer'] = json_load['Items'][0]['Item']['author']
    return info