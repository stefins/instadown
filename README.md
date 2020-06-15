[![Build Status](https://travis-ci.org/IamStefin/Instagram-Image-Downloader.svg?branch=master)](https://travis-ci.org/IamStefin/Instagram-Image-Downloader)

# Instagram Image Downloader

This application  will download all the image from an Instagram public profile

## How to get a query_hash

https://github.com/mineur/instagram-parser/blob/master/docs/setup.md#how-to-get-your-query-hash-old-query-id

## How to use ?

```bash
git clone https://github.com/IamStefin/Instagram-Image-Downloader.git
cd Instagram-Image-Downloader
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py github `your query hash`
```
This will download all post from Github instagram page

Threading is available in `threading` branch

## Running in Docker

In interactive mode

`docker run -it  -v $(pwd):/app/POSTS/ iamstefin/instadown github {your_query_hash}`

In background mode

`docker run -d  -v $(pwd):/app/POSTS/ iamstefin/instadown github {your_query_hash}`


Feel free to make this code better :)
