import requests
import time
import web3
import json

contract = ''
slug = ''
url = 'https://api.opensea.io/api/v1/events'

loop = True

def startBot():
    print('-- -- --')
    print('Started bot!')
    print('Created by @angolcrypto for Twitter')
    print('-- -- --')
    while loop == True:
        print(checkSales())
        time.sleep(280)

etherscan_template = 'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash=0x5bf25a7d8c5edf8e083a6fc8a46021768f8855f4ba996a6eac2a577a2688c76e&apikey=DT73NBDXHV6F8VYI4AWZD6BQUPN6MVATE1'

def checkSales():
    # Variables
    onlyAfterTime = int(time.time())-int(280)

    # Request Data
    querystring = {"asset_contract_address":"0x0B0b186841C55D8a09d53Db48dc8cab9dbf4Dbd6","collection_slug":"satoshibles","event_type":"successful","only_opensea":"false","offset":"0","limit":"30","occurred_after":str(onlyAfterTime)}
    headers = {"Accept": "application/json"}

    # Functions
    response = requests.request("GET", url, headers=headers, params=querystring)
    rj = json.loads(response.text)
    print(rj)

    # Final Values
    sales = []
    for sale in rj['asset_events']:
        _image = sale['asset']['image_url']
        _name = sale['asset']['name']
        _price = float(web3.Web3.fromWei(int(sale['total_price']),'ether'))
        _url = sale['asset']['permalink']
        print('NEW SALE!')
        print(_image)
        print(_name)
        print(_url)
        print(str(_price))
        sales.append({'image':_image,'name':_name,'price':_price,'url':_url})

    print('--------------')
    print('--------------')
    print('Complete check!')
    print('--------------')
    print('--------------')
    return sales

def makeTweet():
    print('Tweet, tweet!')

startBot()
