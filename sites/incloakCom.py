import requests
import re
import sys
from bs4 import BeautifulSoup as bs

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from ProxyPool import Proxy, addProxy

def crawl():
  counter = 1
  while True:
    print "{} Starting crawling. counts {}".format(sys.modules[__name__].__file__, counter)
    try:
      RE_Pattern_IPaddr = re.compile("[0-9\.].*")
      soup = bs(requests.get("https://incloak.com/proxy-list/?anon=4#list").content,"html.parser")

      for RAW_ProxyInfo in soup.find_all("tr"):
        #Length is checked so not to include the skeleton frame <td>
        if len(RAW_ProxyInfo.find_all("td")) == 7:
          IP = str(RAW_ProxyInfo.find("td",{"class":"tdl"})).replace("<td class=\"tdl\">","").replace("</td>","")
          PORT = str(RAW_ProxyInfo.find("td",None)).replace("<td>","").replace("</td>","")
          PROTOCOL = RAW_ProxyInfo.find_all("td")[4].text.split(",")[0].strip()
          addProxy(Proxy(IP, PROTOCOL, PORT))
      print "{} Finished crawl. counts {}".format(sys.modules[__name__].__file__, counter)
    except Exception as e:
      print "{} Error occurred at {}th cycle. Error is {}".format(sys.modules[__name__].__file__, counter, e)
    counter += 1

if __name__ == "__main__":
  crawl()