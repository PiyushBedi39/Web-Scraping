import pandas as pd
import requests
from bs4 import BeautifulSoup


url ="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
info_list=[]


def getdata(url):
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def getinfo(soup):
    
    products = soup.find_all('div',{'data-component-type' : 's-search-result'})
    for item in products:
        product_name = item.find('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'}).text.strip()
        product_link = 'https://www.amazon.in'+str(item.find('a',{'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href'])
        try:
            price = item.find('span',{'class':'a-price-whole'}).text.strip()
        except:
            price = 'Not available'
        try:
            reviews = item.find('span',{'class':'a-size-base s-underline-text'}).text.replace("-","").strip()
        except:
            reviews = 0
        try:
            rating = item.find('span',{'class':'a-icon-alt'}).text.replace("out of 5 stars","").strip()
        except:
            rating = 'Not rated'
        item_list={'Product Name':product_name,
                    'Price':price,
                    'Rating':rating,
                    'Reviews':reviews,
                    'Link':product_link

        }
        info_list.append(item_list)

def getnextpage(soup):
    #check if next page exists or not
    pages = soup.find('div',{'class':'a-section a-text-center s-pagination-container'})
    
    if not pages.find('span',{'class':'s-pagination-item s-pagination-next s-pagination-disabled'}):
        url = 'https://www.amazon.in'+str(soup.find('div',{'class':'a-section a-text-center s-pagination-container'}).find('a',{'class':'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])
        return url
    else:
        return


while True:

    soup = getdata(url)
    getinfo(soup)
    url = getnextpage(soup)
    
    if not url:
        break
    else:
        print(url)
        
        
df = pd.DataFrame(info_list)


print(df.head())
df.to_csv('webscrape_1.csv',index=False)
