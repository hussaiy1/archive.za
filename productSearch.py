import string
import requests
import json
from datetime import datetime
import threading 
import time
import os

def removeFile(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("File doesn't exists")


alpha = list(string.ascii_uppercase)
numb = list(range(0, 10))
base =  '060601A'

productIds = []

for i in range(len(alpha)):
    for k in range(len(alpha)):
        for y in range(len(numb)):
            for j in range(len(alpha)):
                productId = base + alpha[i] + alpha[k] + alpha[j] + str(numb[y])
                productIds.append(productId)



def productSearch(prodId):
    counter = 0
    try:
        client = requests.Session()
        r = client.get('https://www.archivestore.co.za/product/generateProductJSON.jsp?productId={}'.format(prodId))
        time.sleep(1)
        productData = json.loads(r.text)
        if len(productData) > 0:
            name = productData['name']
            with open('productList.csv', 'a') as f:
                f.write('{}|{} \n'.format(prodId, name))
                f.close()
            print('{} - {}'.format(prodId, name))
        else:
            print('{} - Can;t find this'.format(prodId))

    except requests.exceptions.ConnectionError:
        print('Unable to find product at ID: {}'.format(prodId))
        with open('emptyID.txt', 'a') as f:
            f.write('{} \n'.format(prodId))
            f.close()
    counter += 1
    if counter % 100 == 0:
        time.sleep(300)


threads = []
split = 1000


x=0

with open('productList.csv', 'w') as f:
    f.write('product_id|product_name')
    f.close

removeFile('productList.csv')
removeFile('emptyID.txt')
while x<998:
    for i in range(len(productIds[(x*176):(x+1)*176])):
        t = threading.Thread(target=productSearch, args=(productIds[(x*176):(x+1)*176][i],))
        threads.append(t)
        t.start()
    for one_thread in threads:
        one_thread.join()
    x += 1


dateTimeObj = datetime.now()
print(str(dateTimeObj))
print(productIds[(x*176):(x+1)*176])

