import requests
from copy import deepcopy
from os import system as cmd
from time import sleep

REQ_TIMEOUT = 5

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
  if testConnection(proxy):
    proxy_set.add(proxy)
    print "[ProxyPool] added {}".format(proxy)
    return True
  else:
    print "[ProxyPool] not added. {} is not anomynous".format(proxy)
    return False

#*Delete Proxy Data with no connection
def cleanNonWorking():
  global proxy_set
  print "[ProxyPool][Start] cleanning proxy set"
  getProxyPoolStatus(proxy_set)
  proxy_set_cloned = deepcopy(proxy_set)
  originIP = getOriginIP()
  for proxy in proxy_set_cloned:
    isAnonymous = testConnection(proxy, originIP)
    if isAnonymous == False:
      print "removing proxy {}".format(proxy)
      proxy_set.remove(proxy)
    sleep(0.5)
  print "[ProxyPool][Done] cleanning proxy set"
  getProxyPoolStatus(proxy_set)
  sleep(10)

#Outputs Total number of Proxies within ProxyPoolDB, Rate of Proxy HealthChecks, Num of Threads active, Rate of new Proxies added, Rate of Health Proxies
def getProxyPoolStatus(proxy_set):
  print "[ProxyPool] Proxy Amount: "+str(len(proxy_set))

def getOriginIP():
  originIP = None
  for attempt in xrange(3):
    try:
      originIP = requests.get("http://wenhang.net/ipcheck", timeout=REQ_TIMEOUT).content.split(";")[0]
    except Exception as e:
      print "Attempt {}. Failed to retrieve origin ip {}".format(attempt+1, e)
    break
  return originIP

#Testing given Proxy's connection and anonymity, returns True if it can be used and is anonymous, otherwise returns False
def testConnection(proxy, originIP = None):
  proxies = { proxy.protocol: proxy.ip+":"+proxy.port }
  try:
    if originIP == None:
      originIP = getOriginIP()

    if originIP == None:
      raise Exception("Failed to get origin IP")

    maskedIPs = requests.get("http://wenhang.net/ipcheck", timeout=REQ_TIMEOUT, proxies=proxies).content.replace(";", " ").split(" ")
    if originIP in maskedIPs:
      return False
    else:
      return True
  except Exception as e:
    print e 
    return False 
