#merging csv files
import pandas as pd

df1 = pd.read_csv("inner_amazon.csv")
df1.insert(0,"S.No.",range(1,1+len(df1)))

df2 = pd.read_csv("webscrape_1.csv")
df2.insert(0,"S.No.",range(1,1+ len(df2)))

df3 = pd.merge(df2,df1,on='S.No.',how='outer')
df3.to_csv("web_scraping_data.csv",header=True,index=False)