import requests
from copy import deepcopy
from os import system as cmd
from time import sleep
import pickle

REQ_TIMEOUT = 5

BACKUP_FILE_PATH = '/tmp/'
BACKUP_FILE_NAME = 'proxy.pickle'

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
    print "[ProxyPool]################ added {} ##############################".format(proxy)
    return True
  else:
    print "[ProxyPool] not added. {} is not anomynous".format(proxy)
    return False

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

def getProxyPoolStatus(proxy_set):
  print "[ProxyPool] Proxy Amount: "+str(len(proxy_set))

def getOriginIP():
  originIP = None
  for attempt in xrange(3):
    try:
      originIP = requests.get("http://wenhang.net/ipcheck", timeout=REQ_TIMEOUT).content.split(";")[0]
      break
    except Exception as e:
      print "Attempt {}. Failed to retrieve origin ip {}".format(attempt+1, e)
  return originIP

def testConnection(proxy, originIP = None):
  proxies = { proxy.protocol: proxy.ip+":"+proxy.port }
  try:
    if originIP == None:
      originIP = getOriginIP()

    if originIP == None:
      raise Exception("Failed to get origin IP so cannot test connection")

    maskedIPs = requests.get("http://wenhang.net/ipcheck", timeout=REQ_TIMEOUT, proxies=proxies).content.replace(";", " ").split(" ")
    if originIP in maskedIPs:
      print "Original IP. {} \n Masked IPs {} \n Proxies {}".format(originIP, maskedIPs, proxies)
      return False
    else:
      return True
  except Exception as e:
    print e 
    return False 

# Dump proxy_set to file
def dump():
  with open("{}{}".format(BACKUP_FILE_PATH, BACKUP_FILE_NAME), 'w') as f:
    pickle.dump(proxy_set, f)

# Restore proxy_set
def restore():
  global proxy_set
  with open("{}{}".format(BACKUP_FILE_PATH, BACKUP_FILE_NAME)) as f:
    proxy_set = pickle.load(f)


