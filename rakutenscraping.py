import os
from bs4 import BeautifulSoup
from urllib import request
import requests
import datetime
import time
from time import sleep
import schedule
FLinks=["0"]
path="f.txt"
with open(path) as f:
    FLinks=f.read()

print(FLinks)
def SendToDiscord(Sentcontents):
  webhook_url = ''
 
  main_content = {
    "content": Sentcontents
    }
  requests.post(webhook_url,main_content)

def LinkCollect():
  Rakuurl = 'https://www.rakuten-sec.co.jp/web/market/fisco/'
  html = request.urlopen(Rakuurl)
  soup = BeautifulSoup(html,"html.parser")
  Links=[]
  # tag_list = soup.select('a[href*="fisco/"]　')
  tag_list =soup.find_all('a')
  
  for tag in tag_list:
    url = tag.get('href')
    if "/web/market/fisco/detail/" in url:
      Links.append("https://www.rakuten-sec.co.jp"+url)
      
    else:
      continue
    print(Links)
    return Links


#10分に1回にする
def LinkScrape(Links,FLinks):
  # i=0 #実行ごとに0に指定する必要あり
  # while Links[i]!=FLinks:
  #   print(i)
  #fから読み込んだリンクと違った場合（更新されている場合）
  if Links[0] !=FLinks:
    ForHtml=request.urlopen(Links[0])
    Fsoup = BeautifulSoup(ForHtml,"html.parser")
    title=Fsoup.find("h2")
    Japtitle=title.text
    Japtitle.replace("\r","")
    xcc=[]
    contents=Fsoup.find('div', id="str-main")
    con=contents.find("p")
    cc=con.text
    ccc=cc.replace("【株式会社フィスコ】","") .replace(" ","").replace("　","").replace("《KK》","")
    Sentcontents=str(Japtitle)+"\n"+str(ccc)+Links[0]
    SendToDiscord(Sentcontents)
    return Sentcontents
  else:
    return

#ここまででループ終わり

def main():
  try:
    Links=LinkCollect()
    print("DOING")
    if FLinks!=Links[0]: #取得しているリンクの一番上と前のリンクが一致していない場合に関数を実行する
      LinkScrape(Links,FLinks)
      with open(path,mode="w") as p:
        p.write(Links[0])
      print("DONE")
    else:
      print("No Last News")
      return
  except Exception as e:
    print(e)

# schedule.every(5).minutes.do(job) #scheduleで5分ごとに設定
# while True:
#   print("実行中")
#   print(FLinks)
#   schedule.run_pending()
#   sleep(60)

 

if __name__ == "__main__":
  main()

