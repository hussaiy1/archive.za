import requests
from bs4 import BeautifulSoup
import json
from discord import *
from colorama import init
from colorama import Fore, Back, Style
from datetime import datetime

init(autoreset=True)

def timeStamp():
    dateTimeObj = datetime.now()
    return str(dateTimeObj)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
with open ('productid.json', 'r') as f:
    productIdList=json.load(f)
    f.close()

productIdList = productIdList['productIDs']
productId=[]
while True:
    for i in range(len(productIdList)):
        productId.append(productIdList['product' + str(i)]['id'])
        client = requests.Session()
        r=client.get('https://www.archivestore.co.za/product/generateProductJSON.jsp?productId={}'.format(productId[i]))
        soup = BeautifulSoup(r.text, 'lxml')
        productData = json.loads(r.text)
        if len(productData) == 0:
            print(Fore.RED + '[{}] Product Not Found'.format(timeStamp()))
        else:
            variants = productData['sizes']
            for j in range(len(variants)):
                name = productData['name']
                size = productIdList['product' + str(i)]['size']
                for k in range(len(size)):
                    if productData['sizes'][j]['name'] == size[k] and productData['sizes'][j]['available']==True:
                        print(Fore.GREEN +'[{}] Product In Stock, {} Size {}'.format(timeStamp(),name, size[k]))
                        sendHook(name,'https://www.archivestore.co.za' + productData['pdpURL'], size[k], productData['images'][0]['thumb'])
                    else:
                        print(Fore.YELLOW +'[{}] Product Out Of Stock, {} Size {}'.format(timeStamp(),name, size[k]))
#
#
#size = '10'
#
#
#
#
##soup = BeautifulSoup(r.text, 'lxml')
#
#productData = json.loads(r.text)
#variants = productData['sizes']
#
#for i in range(len(variants)):
#    if productData['sizes'][i]['name'] == size:
#        print(productData['sizes'][i]['available'])
#
#JSESSIONID = r.cookies['JSESSIONID']
#
#
#payload = {
#    '/atg/commerce/order/purchase/CartModifierFormHandler.addItemToOrder': 'Add to Cart',
#    '_DARGS' : }
#
#
#atc_URL = 'https://www.archivestore.co.za/basket/gadgets/;jsessionid={}?_DARGS=/basket/gadgets/addToCartFromPDP.jsp.addToCartForm'.format(JSESSIONID)
#

