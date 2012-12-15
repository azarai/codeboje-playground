import urllib3
import re
import sys

## Download all palletes favoured by the user.
## requires urllib3
## Tested with python 3.3 64bit on Windows 7
COLOUR_LOVERS_URL = "http://www.colourlovers.com"

def login(http, username, password):
    r = http.request('GET', COLOUR_LOVERS_URL) 
    cookies = r.headers['set-cookie']
    print(r.headers['set-cookie'])
    fields = {'r': 'http%3A%2F%2Fwww.colourlovers.com%2F', 'userName': username, 'userPassword': password, 'x': '46','y':'24'}
    r = http.request('POST', 'https://www.colourlovers.com/op/log-in', fields=fields, headers={ 'Cookie': r.headers['set-cookie']})
    return cookies

if(len(sys.argv) < 3):
    print("Please provide a username and password")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

page = 1

download = True
http = urllib3.PoolManager()
cookies = login(http, username, password)

while (download):
    url = COLOUR_LOVERS_URL + "/ajax/search-palettes/_page_%s?sortCol=date&sortBy=desc&query=&userName=%s&hex=&hueOptions=&f=1&publishedBeginDate=12/27/2000&publishedEndDate=12/11/2012" % (page, username)
    r = http.request('GET', url)
    print(r.status)
    print(r.data)
    
    if(r.status == 200):
        if re.match(".*No Results.*", str(r.data)):
            download = False
        else:
            for palette_id in re.findall(r"p--(?P<palette_id>[0-9]*)-\w{,8}-overlay", str(r.data)):
                url_zip  = COLOUR_LOVERS_URL + "/export/p/zip/%s" % palette_id
                zipdata = http.request('GET', url_zip, headers= {'Cookie': cookies}, redirect=True)
                filename = re.search('name="(.*)"', zipdata.headers['content-disposition']).group(1)
                print(filename.replace('*', ''))
                f = open("%s" % filename.replace('*', ''), 'wb')
                f.write(zipdata.data)
                f.close()
            page+= 1
    else:
        download = False
    
