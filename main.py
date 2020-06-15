#!/usr/bin/env python3
import json
from bs4 import BeautifulSoup
import requests
import re
import wget
import os
import sys
from link import get_link_by_end

image_counter = 0
video_counter = 0

def download_content(uid, username):
    url = "https://www.instagram.com/p/"+str(uid)
    html_doc = requests.get(url,headers=headers,timeout=5).text
    try:
        download_video(html_doc, username)
    except:
        download_img(html_doc, username)

def download_video(html_doc,username):
    result = re.search('"og:video" content="(.*)"', html_doc)
    link = result.group(1)
    print('Downloading Video')
    name=wget.download(link,'POSTS/'+username+'/')
    print(name)
    global video_counter
    video_counter += 1

def download_img(html_doc,username):
    result = re.search('"og:image" content="(.*)"', html_doc)
    link = result.group(1)
    print('Downloading Image')
    name=wget.download(link,'POSTS/'+username+'/')
    print(name)
    global image_counter
    image_counter += 1

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
    username = sys.argv[1]
    query_hash = sys.argv[2]
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
    sency,endlink=get_link_by_end(get_end_cursor(uid),account_id,query_hash)
    while True:
        for k in sency:
            download_content(k, username)
        sency,endlink=get_link_by_end(endlink,account_id,query_hash)
except:
    print("\n\n" + str(image_counter) + " Images Downloaded!!")
    print(str(video_counter) + " Videos Downloaded!!")
