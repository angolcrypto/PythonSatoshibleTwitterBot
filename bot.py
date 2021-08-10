import requests
import time
import web3
import json
import numpy as np
import tweepy
import shutil

contract = ''
slug = ''
url = 'https://api.opensea.io/api/v1/events'

consumer_key=''
consumer_secret_key=''
access_token=''
access_token_secret=''

auth=tweepy.OAuthHandler(consumer_key,consumer_secret_key)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)

loop = True

def startBot():
    print('-- -- --')
    print('Started bot!')
    print('Created by @angolcrypto for Twitter')
    print('-- -- --')
    while loop == True:
        checkSales()
        time.sleep(280)

etherscan_template = 'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash=0x5bf25a7d8c5edf8e083a6fc8a46021768f8855f4ba996a6eac2a577a2688c76e&apikey='

def checkSales():
    # Variables
    onlyAfterTime = int(time.time())-int(280)

    # Request Data
    querystring = {"asset_contract_address":"0x0B0b186841C55D8a09d53Db48dc8cab9dbf4Dbd6","collection_slug":"satoshibles","event_type":"successful","only_opensea":"false","offset":"0","limit":"30","occurred_after":str(onlyAfterTime)}
    headers = {"Accept": "application/json"}

    # Functions
    response = requests.request("GET", url, headers=headers, params=querystring)
    rj = json.loads(response.text)

    # Final Values
    for sale in rj['asset_events']:
        _image = sale['asset']['image_url']
        _name = sale['asset']['name']
        _price = float(web3.Web3.fromWei(int(sale['total_price']),'ether'))
        _url = sale['asset']['permalink']

        makeTweet(_name, _url, _image, _price)

    print('Checked Sales')

def makeTweet(name, url, image, price):
    # Text only tweet:
    # api.update_status('Testing the Developer API!')
    text = f"{name} bought for {price}ETH 🚀 #nft #crypto #satoshibles #nfts"

    response = requests.get(image, stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    del response

    # API.update_with_media(filename[, status][, in_reply_to_status_id][, auto_populate_reply_metadata][, lat][, long][, source][, place_id][, file])
    api.update_with_media('img.png', text)
    print('Tweeted')

startBot()
