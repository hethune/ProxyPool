import re
import requests
import base64
import time
from bs4 import BeautifulSoup as bs

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from ProxyPool import Proxy, addProxy

REQ_TIMEOUT = 3

def crawl():
  '''
  This is the script for scraping http://proxy-list.org site
  '''

  BASE_URL = "https://proxy-list.org/english/index.php?p=" 

  Re_Pattern_IP = re.compile("(.*):")
  Re_Pattern_PORT = re.compile(":(.*)")

  while True:
    counter = 1
    for startingURL_Param in range(1,11):
      print "{} Starting crawling. counts {}. page {}".format(sys.modules[__name__].__file__, counter, startingURL_Param)
      try:        
        HTML_ProxyPage = requests.get(BASE_URL+str(startingURL_Param), timeout= REQ_TIMEOUT).content
        soup = bs(HTML_ProxyPage,"html.parser")
        for Raw_ProxyInfo in soup.find_all("ul",{"class":None}):
          ip_port = base64.b64decode(Raw_ProxyInfo.find("li",{"class":"proxy"}).text.replace("Proxy('","").replace("')",""))
          IP = re.findall(Re_Pattern_IP, ip_port)[0]
          PORT = re.findall(Re_Pattern_PORT, ip_port)[0]
          PROTOCOL = Raw_ProxyInfo.find("li",{"class":"https"}).text.lower()
          if PROTOCOL in ['http', 'https']:
            addProxy(Proxy(IP, PROTOCOL, PORT))
        print "{} Finished crawl. counts {}. page {}".format(sys.modules[__name__].__file__, counter, startingURL_Param)
      except Exception as e:
        print "{} Error occurred at {} th cycle {} th page. Error is {}".format(sys.modules[__name__].__file__, counter, startingURL_Param, e)
    
    time.sleep(30)

if __name__ == "__main__":
  crawl()