import os

def createlineloginuri(line_clientid):
    uri = ''
    uri += 'https://access.line.me/oauth2/v2.1/authorize?response_type=code'
    uri += line_clientid
    uri += '&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Flinelogin_callback'
    uri += '&state=' + os.urandom(10)
    uri += '&scope=profile%20openid'
    return uri