import requests
import pandas as pd
import time
from random import randrange
from bs4 import BeautifulSoup
page = 1
total_product = 0
loop = True
while loop:
    tiki_link ='https://tiki.vn/dien-thoai-may-tinh-bang/c1789?_lc=Vk4wMzQwMjAwMDQ=&page='
    final_link = tiki_link + str(page)
    html = requests.get(final_link)
    soup = BeautifulSoup(html.text, 'html.parser')

    products = []

    products_item_tag = soup.find_all('div', {'class':'product-item'})

    if products_item_tag == []:
        loop = False

    else:
        print("_"*100)
        print(final_link)
        for product_item_tag in products_item_tag:
            d = {'data-title': '', 'data-price': '', 'data-seller-product-id': '', 'data-id': ''}
            try:
                d['data-title'] = product_item_tag['data-title']
                d['data-price'] = product_item_tag['data-price']
                d['data-seller-product-id'] = product_item_tag['data-seller-product-id']
                d['data-id'] = product_item_tag['data-id']
                # There are some products without img tag...
                if product_item_tag.img:
                    d['image_url'] = product_item_tag.img['src']  # or should we use ['src'] ?

                # Append the dictionary to data list
                products.append(d)

            except:
                # Skip if error and print error message
                print("We got one article error!")
        for product in products:
            print(product)

        print("page"+str(page))
        print(len(products))
        total_product +=len(products)
        page +=1


if len(products) == 0:
    print("Out of products")
else:
    products_data = pd.DataFrame(data = products, columns = products[0].keys())
    print(type(products_data))
    products_data.to_pickle("./new_result.pkl")
    unpickled_result = pd.read_pickle("./new_result.pkl")
    print(unpickled_result)
    products_data.to_csv("./new_result.csv", index=False)

print(total_product)