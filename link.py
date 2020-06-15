import requests,json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
def get_link_by_end(after,idd,query_hash):
    url = 'https://www.instagram.com/graphql/query/?query_hash='+query_hash+'&variables={"id":"'+idd+'","first":50,"after":"'+after+'"}'
    user_doc = requests.get(url,headers=headers,timeout=5).text
    user_doc = json.loads(user_doc)
    links =[]
    for i in range(50):
        links.append(str(user_doc['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']))
    new_endlink= str(user_doc['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'])
    return links,new_endlink
