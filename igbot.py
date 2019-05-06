import time
import requests
import json
from urllib.parse import urlparse

def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return 'False'

url ="https://api.telegram.org/bot886435771:AAG3NZy7S3GUUG17yRNGQqlyaljxGw5NVkI/getUpdates"

previd = 0

while True:
        r = requests.get(url).text
        d=json.loads(r)
        try:
            imgurl=d['result'][-1]['message']['text']
        except:
            imgurl=""
        chatid= d['result'][-1]['message']['from']['id']
        msgid = d['result'][-1]['message']['message_id']
        urll = imgurl
        if is_url(urll)==True:
            if(msgid!=previd):
                try:
                    r = requests.get(urll).text
                    start = '<meta property="og:image" content="'
                    end = '" />'
                    x=r[r.find(start)+len(start):r.rfind(end)]
                    u=""
                    for i in x :
                        if i=='"':
                            break
                        u=u+i
                    requests.get("https://api.telegram.org/bot886435771:AAG3NZy7S3GUUG17yRNGQqlyaljxGw5NVkI/sendPhoto?chat_id="+str(chatid)+"&photo="+u)
                    previd = msgid
                except:
                    print("Errr")

        time.sleep(5)

