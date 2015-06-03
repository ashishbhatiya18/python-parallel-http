from threading import Thread
import urllib.request, sys
from queue import Queue

class HTTPClient:	
	concurrent = 1
	result = {}
	q = Queue()
	def __init__(self, concurrency_level):
		self.concurrent = concurrency_level

	def doWork(self):
		while True:
			url = self.q.get()
			url, urlResponse = self._getResponse(url)
			self._addToResultMap(url, urlResponse)
			self.q.task_done()

	def _getResponse(self,ourl):
		try:
			res = urllib.request.urlopen(ourl)
			return ourl,res
		except:
			return ourl,"error"

	def _addToResultMap(self,url, resp):
		self.result[url] = resp.read().decode('utf-8')

	def request(self,urlData):	
		for i in range(self.concurrent):
			t = Thread(target=self.doWork)
			t.daemon = True
			t.start()
		try:
			for url in urlData:
				self.q.put(url.strip())
			self.q.join()
			return self.result	
		except KeyboardInterrupt:
		    	sys.exit(1)
