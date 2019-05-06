import time
import requests
import json
import urllib

url ="https://api.telegram.org/bot886435771:AAG3NZy7S3GUUG17yRNGQqlyaljxGw5NVkI/getUpdates"

previd = 0

while True:
        r = requests.get(url).text
        d=json.loads(r)
        imgurl=d['result'][-1]['message']['text']
        chatid= d['result'][-1]['message']['from']['id']
        msgid = d['result'][-1]['message']['message_id']
        urll = imgurl
        if imgurl=='/start' or imgurl=='/stop':
                pass
        elif(msgid!=previd):
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
        time.sleep(5)
        
