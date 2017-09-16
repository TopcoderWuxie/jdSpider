#coding: utf-8

import redis
from log_save import logging_save



class DataSave(object):

	def __init__(self,):
		try:
			self.filename = __file__.split("\\")[-1].split(".")[0]
		except Exception as e:
			self.filename = __file__.split("/")[-1].split(".")[0]
		self.host = 'localhost'  
		self.port = 6379
		self.db = "shop_urls"
		self.password = "root"
		self.saveData = set([])

	def addData(self, url):
		self.saveData.add(url)

	def write(self,):
		try:
			r = redis.StrictRedis(host= self.host, port= self.port, password= self.password)
			r.set(self.db, self.saveData)
		except Exception as e:
			print(e)
			logging_save("- {} - 数据插入redis数据库出错 {}".format(self.filename, e), "ERROR")

if __name__ == "__main__":
	data = DataSave()
	data.write("Hello World!!")