import threading
import time
import sys

class siteThread(threading.Thread):
  def __init__(self, name, crawlerFunc):
    threading.Thread.__init__(self)
    self.name = name
    self.crawlerFunc = crawlerFunc

  def run(self):
    self.crawlerFunc()

class proxyThread(threading.Thread):
  def run(self):
    import ProxyPool

    print "starting proxy pools"
    while True:
      ProxyPool.cleanNonWorking()

class proxyDumpThread(threading.Thread):
  def run(self):
    import ProxyPool

    print "starting proxy dump thread"
    while True:
      ProxyPool.dump()
      print "[Deamon] Dumped proxies"
      time.sleep(30)

def makeSiteThreads():
  import pkgutil
  import sites

  sites_modules = []
  for importer, modname, ispkg in pkgutil.iter_modules(sites.__path__):
    sites_modules.append(importer.find_module(modname).load_module(modname))

  site_threads = []
  for m in sites_modules:
    t = siteThread(m.__name__, m.crawl)
    t.deamon = True
    site_threads.append(t)

  return site_threads

if __name__ == "__main__":
  site_threads = makeSiteThreads()

  for t in site_threads:
    t.start()
  
  proxy_t = proxyThread()
  proxy_t.deamon = True
  proxy_t.start()

  proxy_d = proxyDumpThread()
  proxy_d.deamon = True
  proxy_d.start()

  for t in site_threads:
    t.join()

  proxy_t.wait()
  proxy_d.wait()


