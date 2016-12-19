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
    for startingURL_Param in range(1,11):
      while True:
        try:
          #If there's an error duing the request, it will try to reconnect until succeed
          while True:
            try:
              HTML_ProxyPage = requests.get(BASE_URL+str(startingURL_Param), timeout= REQ_TIMEOUT).content
              break
            except Exception as e:
              pass
          soup = bs(HTML_ProxyPage,"html.parser")
          for Raw_ProxyInfo in soup.find_all("ul",{"class":None}):
            ip_port = base64.b64decode(Raw_ProxyInfo.find("li",{"class":"proxy"}).text.replace("Proxy('","").replace("')",""))
            IP = re.findall(Re_Pattern_IP, ip_port)[0]
            PORT = re.findall(Re_Pattern_PORT, ip_port)[0]
            PROTOCOL = Raw_ProxyInfo.find("li",{"class":"https"}).text.lower()
            if PROTOCOL in ['http', 'https']:
              addProxy(Proxy(IP, PROTOCOL, PORT))
          break
        except Exception as e:
          print "An error occurred: "+str(e)
    print "[ Done Fetching {} Sleep for 30 seconds... ]".format(BASE_URL)
    time.sleep(30)
    print ""

if __name__ == "__main__":
  crawl()