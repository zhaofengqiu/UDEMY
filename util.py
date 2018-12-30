import threadpool 
import requests
# import time 
def sayhello(item):
	global source_list
	item = item[0]
	r=requests.get(url= item[1],headers= item[2])
	if abs(int(r.headers["Content-Length"])- len(r.content))>100:
		r=requests.get(url= item[1],headers= item[2])
	if abs(int(r.headers["Content-Length"])- len(r.content))< 100:
		if len(source_list)==0:
			print("source_list",source_list)
		source_list[item[0]] = r.content
	else:
		source_list[item[0]] = "unsuccess"
class My_download_thread():
	def __init__(self,source_url,downloadsuns):
		global source_list
		source_list=[]
		self.source_url =source_url
		self.downloadsuns = downloadsuns
	def get_bytes_source(self):
		size  = self.get_source_size()
		self.get_source_list(size)
		arg_list=[]
		source_url_list = [self.source_url]*len(source_list)
		for i in range(len(source_url_list)):
			arg_list.append([(i,source_url_list[i],source_list[i])])
		pool = threadpool.ThreadPool(self.downloadsuns) 
		requests = threadpool.makeRequests(sayhello,list(arg_list)) 
		[pool.putRequest(req) for req in requests]
		pool.wait() 
		if "unsuccess" in source_list:
			flag = False
		else:
			flag = True
		content=b''
		for source in source_list:
			content+=source
		return flag,content
	def get_source_size(self):
		headers={"Range":"bytes=0-100"}
		r=requests.get(self.source_url,headers=headers)
		return int(r.headers['Content-Range'].split("/")[-1])
	def get_source_list(self,size):
		global source_list
		lis = list(range(self.downloadsuns))
		li =[]
		for l in lis:
			li.append({"Range":"bytes=%d-%d"%(l*size//self.downloadsuns,(l+1)*size//self.downloadsuns)})
		source_list = li
