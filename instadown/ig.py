#!/usr/bin/env python3
import json
import logging
import os
import re
import sys
from collections import namedtuple
from typing import List

import requests
import wget

Media = namedtuple('Media', 'source_type url')

logging.basicConfig(level=logging.INFO)
image_counter = 0
video_counter = 0


def download_content(uid, username):
    url = f"https://www.instagram.com/p/{uid}"
    html_doc = requests.get(url, headers=headers, timeout=5).text
    # download both images and videos
    download_medias(html_doc, username)


def download_medias(html_doc, username):
    global image_counter
    global video_counter
    # collector of media urls (could be both images and videos)
    media_list: List[Media] = []
    # parse the returned html body response and loads it as a json string
    json_string = re.search('window._sharedData = (.*);</script>', html_doc).group(1)
    as_json = json.loads(json_string)
    # identify the json entry we have to work with
    entry = as_json["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
    # look for key 'edge_sidecar_to_children' (multiple images/videos)
    if 'edge_sidecar_to_children' in entry:
        # find edges
        sidecar_edges = entry["edge_sidecar_to_children"]["edges"]
        sidecar_edges = [edge for edge in sidecar_edges]
        # find nodes
        sidecar_nodes = [edge['node'] for edge in sidecar_edges]
        # loop over nodes and collect images and videos
        for node in sidecar_nodes:
            if node['is_video']:
                media_list.append(Media(source_type='video', url=node['video_url']))
            else:
                media_list.append(Media(source_type='image', url=node['display_url']))
    else:
        # must be a single media
        if entry['is_video']:
            media_list.append(Media(source_type='video', url=entry['video_url']))
        else:
            media_list.append(Media(source_type='image', url=entry['display_url']))

    for source_type, url in media_list:
        logging.info(f'Downloading {source_type} from {url}')
        name = wget.download(url, 'POSTS/' + username + '/')
        logging.info("\n" + name)

        if source_type == 'video':
            video_counter += 1
        else:
            image_counter += 1


def get_end_cursor(uid):
    url = "https://www.instagram.com/p/" + str(uid)
    user_doc = requests.get(url, headers=headers, timeout=5).text
    json_data = re.search('window._sharedData = (.*);</script>', user_doc).group(1)
    d = json.loads(json_data)
    end_cursor = str(
        d['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['page_info'][
            'end_cursor'])
    return end_cursor


def get_link_by_end(after, idd, query_hash):
    url = 'https://www.instagram.com/graphql/query/?query_hash=' + query_hash + '&variables={"id":"' + idd + '","first":50,"after":"' + after + '"}'
    user_doc = requests.get(url, headers=headers).text
    user_doc = json.loads(user_doc)
    links = []
    for i in range(50):
        links.append(str(user_doc['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']))
    new_endlink = str(user_doc['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'])
    return links, new_endlink


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def main():
    if len(sys.argv) > 3:
        print('You have specified too many arguments')
        sys.exit()
    elif len(sys.argv) == 1 or len(sys.argv) == 2:
        print("Usage: \n")
        print("instadown 'user_name' 'query_hash'")
        sys.exit()
    try:
        username = sys.argv[1]
        query_hash = sys.argv[2]
        try:
            os.mkdir('POSTS/')
        except:
            pass
        try:
            os.mkdir('POSTS/' + username + '/')
        except:
            pass
        url = "https://www.instagram.com/" + username
        user_doc = requests.get(url, headers=headers).text
        json_data = re.search('window._sharedData = (.*);</script>', user_doc).group(1)
        d = json.loads(json_data)
        account_id = str(d['entry_data']['ProfilePage'][0]['graphql']['user']['id'])
        end_cursor = str(
            d['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'])
        uid = d['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][0]['node'][
            'shortcode']
        sency, endlink = get_link_by_end(get_end_cursor(uid), account_id, query_hash)
        while True:
            for k in sency:
                try:
                    download_content(k, username)
                except requests.exceptions.ReadTimeout:
                    logging.info("Download Failed!!")
            try:
                sency, endlink = get_link_by_end(endlink, account_id, query_hash)
            except requests.exceptions.ReadTimeout:
                logging.info("End link fetching failed!!")
    except requests.exceptions.ReadTimeout:
        logging.info("\n\n" + str(image_counter) + " Images Downloaded!!")
        logging.info(str(video_counter) + " Videos Downloaded!!")
    except KeyboardInterrupt:
        logging.info("\n\n" + str(image_counter) + " Images Downloaded!!")
        logging.info(str(video_counter) + " Videos Downloaded!!")
    except:
        logging.info("\nOops! Some Error Occured!!")

if __name__ == '__main__':
    main()
