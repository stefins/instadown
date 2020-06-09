#!/usr/bin/env python3
import json
from bs4 import BeautifulSoup
import requests
import re
import wget
import os
from link import get_link_by_end
import threading
import time

def download_img(uid,username):
    url = "https://www.instagram.com/p/"+str(uid)
    html_doc = requests.get(url,headers=headers,timeout=5).text
    result = re.search('"og:image" content="(.*)"', html_doc)
    link = result.group(1)
    name=wget.download(link,'POSTS/'+username+'/')
    print(name)

def get_end_cursor(uid):
    url = "https://www.instagram.com/p/"+str(uid)
    user_doc = requests.get(url,headers=headers,timeout=5).text
    json_data = re.search('window._sharedData = (.*);</script>',user_doc).group(1)
    d = json.loads(json_data)
    end_cursor = str(d['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor'])
    return end_cursor

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

try:
    counter = 0
    username = input("Enter The Username : ")
    try:
        os.mkdir('POSTS/')
    except:
        pass
    try:
       os.mkdir('POSTS/'+username+'/')
    except:
	    pass
    url = "https://www.instagram.com/"+username
    user_doc = requests.get(url,headers=headers,timeout=5).text
    json_data = re.search('window._sharedData = (.*);</script>',user_doc).group(1)
    d = json.loads(json_data)
    account_id = str(d['entry_data']['ProfilePage'][0]['graphql']['user']['id'])
    end_cursor = str(d['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'])
    uid= d['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['shortcode']
    sency,endlink=get_link_by_end(get_end_cursor(uid),account_id)
    while True:
        for k in sency:
            try:
                t1 = threading.Thread(target=download_img, args=(k,username,))
                t1.start()
            except:
                print("Some Error Occured :(")
            counter += 1
        try:
            sency,endlink=get_link_by_end(endlink,account_id)
            t1.join()
        except:
            print("Some Error Occured ;(")
except:
    print("\n\n"+str(counter)+" Images Downloaded!!")
