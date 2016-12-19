import requests
from copy import deepcopy
from os import system as cmd
from time import sleep

REQ_TIMEOUT = 2

proxy_set = set()

class Proxy:
  def __init__(self, ip, protocol, port):
    self.ip = ip
    self.protocol = protocol
    self.port = port

  def __str__(self):
    return "{}://{}:{}".format(self.protocol, self.ip, self.port)

  def __hash__(self):
    return hash(str(self))

  def __eq__(self, other):
    return ((self.ip, self.protocol, self.port) == (other.ip, other.protocol, other.port))


#Add record if not exist
def addProxy(proxy):
  global proxy_set
  print "adding proxy"
  print "Proxy size is {}".format(len(proxy_set))
  proxy_set.add(proxy)

#*Delete Proxy Data with no connection
def cleanNonWorking():
  global proxy_set
  proxy_set_cloned = deepcopy(proxy_set)
  for proxy in proxy_set_cloned:
    getProxyPoolStatus(proxy_set_cloned)

    isAnonymous = testConnection(proxy)
    if isAnonymous == False:
      proxy_set.remove(proxy)

#Outputs Total number of Proxies within ProxyPoolDB, Rate of Proxy HealthChecks, Num of Threads active, Rate of new Proxies added, Rate of Health Proxies
def getProxyPoolStatus(proxy_set):
  print "[!] Proxy Amount: "+str(len(proxy_set))

#Testing given Proxy's connection and anonymity, returns True if it can be used and is anonymous, otherwise returns False
def testConnection(proxy, originalIP = None):
  proxies = { proxy.protocol: proxy.ip+":"+proxy.port }
  try:
    if originalIP == None:
      originalIP = requests.get("http://wenhang.net/ipcheck", timeout=REQ_TIMEOUT).content.split(";")[0]

    maskedIPs = requests.get("http://wenhang.net/ipcheck", timeout=REQ_TIMEOUT, proxies=proxies).content.replace(";", " ").split(" ")
    if originalIP in maskedIPs:
      return False
    else:
      return True
  except Exception as e:
    print e 
    return False 
  sleep(0.5)
