#Scrape inner data from url in csv
import pandas as pd
from bs4 import BeautifulSoup
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
info_list=[]


def getdata(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def getinfo(soup):
    
    try:
        description = soup.find('ul',class_="a-unordered-list a-vertical a-spacing-mini").text.strip()
    except:
        description = "No description"


    try:
        asin=soup.find('div',id='averageCustomerReviews').attrs['data-asin']
    except:
        asin="error"


    try:
        try:
            product_description= soup.find('div',id='productDescription').find('span').text.strip()
            
        except:
            product_desc = soup.find('div',class_="a-expander-content a-expander-partial-collapse-content").find_all("tr")
            product_description=product_desc[1].text.strip()
            
    except:
        product_description='Not Mentioned'
    


    try:
        details_for_manufacturer=soup.find('div', id='detailBullets_feature_div').find('ul').find_all('li')
        manufacturer=""
        for item in details_for_manufacturer:
            a=item.find('span',class_='a-text-bold').text.strip()

            if a.lower().find('manufacturer')==0:
                manufacturer=item.find('span',class_='a-list-item').find_all('span')[1].text
                break
            
    except:   
        manufacturer="Unknown"
    item_list={"Description":description,
                "ASIN":asin,
                "Product Description":product_description,
                "Manufacturer":manufacturer
    }
    info_list.append(item_list)

df = pd.read_csv("webscrape_1.csv")
all_links=df["Link"]


for url in all_links[:251]:
    soup= getdata(url)
    getinfo(soup)
    print(url)
    
df1=pd.DataFrame(info_list)
print(df1.head())
df1.to_csv("inner_amazon.csv",index=False)





