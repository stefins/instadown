#!/usr/bin/env python3
import json
from bs4 import BeautifulSoup
import requests
import re
import wget
import os
import logging
import sys

logging.basicConfig(level=logging.INFO)
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
    logging.info('Downloading Video')
    name=wget.download(link,'POSTS/'+username+'/')
    logging.info(name)
    global video_counter
    video_counter += 1

def download_img(html_doc,username):
    img_list = []
    json_data = re.search('window._sharedData = (.*);</script>',html_doc).group(1)
    d = json.loads(json_data)
    co =0
    while True:
        try:
            img_list.append(d["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"][co]["node"]["display_url"])
            co+=1
        except:
            break
    for link in img_list:
        logging.info('Downloading Image')
        name=wget.download(link,'POSTS/'+username+'/')
        logging.info("\n"+name)
        global image_counter
        image_counter += 1

def get_end_cursor(uid):
    url = "https://www.instagram.com/p/"+str(uid)
    user_doc = requests.get(url,headers=headers,timeout=5).text
    json_data = re.search('window._sharedData = (.*);</script>',user_doc).group(1)
    d = json.loads(json_data)
    end_cursor = str(d['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor'])
    return end_cursor

def get_link_by_end(after,idd,query_hash):
    url = 'https://www.instagram.com/graphql/query/?query_hash='+query_hash+'&variables={"id":"'+idd+'","first":50,"after":"'+after+'"}'
    user_doc = requests.get(url,headers=headers).text
    user_doc = json.loads(user_doc)
    links =[]
    for i in range(50):
        links.append(str(user_doc['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']))
    new_endlink= str(user_doc['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'])
    return links,new_endlink


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def main():
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
        user_doc = requests.get(url,headers=headers).text
        json_data = re.search('window._sharedData = (.*);</script>',user_doc).group(1)
        d = json.loads(json_data)
        account_id = str(d['entry_data']['ProfilePage'][0]['graphql']['user']['id'])
        end_cursor = str(d['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'])
        uid= d['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][0]['node']['shortcode']
        sency,endlink=get_link_by_end(get_end_cursor(uid),account_id,query_hash)
        while True:
            for k in sency:
                try:
                    download_content(k, username)
                except requests.exceptions.ReadTimeout:
                    logging.info("Download Failed!!")
            try:
                sency,endlink=get_link_by_end(endlink,account_id,query_hash)
            except requests.exceptions.ReadTimeout:
                logging.info("End link fetching failed!!")
    except requests.exceptions.ReadTimeout:
        logging.info("\n\n" + str(image_counter) + " Images Downloaded!!")
        logging.info(str(video_counter) + " Videos Downloaded!!")
    except KeyboardInterrupt:
        logging.info("\n\n" + str(image_counter) + " Images Downloaded!!")
        logging.info(str(video_counter) + " Videos Downloaded!!")

if __name__ == "__main__":
    main()