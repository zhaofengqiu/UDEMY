import requests
import time
import os
import re
import threading
from config import *
from queue import Queue
import urllib3
urllib3.disable_warnings()
qc = Queue()
session = requests.session()
session.headers.update(HEADERS)
downloadlist = Queue()
class Contain():

    def __init__(self,name,data):
        self.data = data
        self.name = name
        self.lectures = []
    def add(self,data):
        self.lectures.append(data)
class Mythread(threading.Thread):
    def __init__(self,qc,orgin,course_id):
        threading.Thread.__init__(self)
        self.queue = qc
        self.orgin = orgin
        self.course_id=course_id
    def run(self):
        while not qc.empty():
            chapter=qc.get()

            relative_path = get_creat_path(self.orgin,str(chapter.data["object_index"])+"-"+chapter.data["title"])

            creat_dir(relative_path)
            for lecture in chapter.lectures:
                msg=get_video_message(self.course_id,lecture["id"])
                if "none" != msg["name"] and "mp4" in msg["url"]:

                    video_name = get_creat_path(self.orgin,str(chapter.data["object_index"])+"-"+chapter.data["title"],filename=str(lecture["object_index"])+"-"+msg["name"])
                    down_load_mp4(msg["url"],video_name)
def is_int(data):
    if isinstance(data,int):
        return False
    else:
        return True

def get_ts(m3n8s):
    li = []
    for item in m3n8s:
        if "ts" in item:
            li.append(item)
    return li
def get_tree(course_id):
    chapters=list(range(100))
    index=0
    url = VIDEOS_IDS_GET_URL.replace("course_id",str(course_id))
    resp=session.get(url)
    jsons = resp.json()
    for data in jsons["results"]:
        if data["_class"] == "chapter":
            chapter = Contain(data["title"],data)
            index = data["object_index"]
            chapters.insert(data["object_index"],chapter)
        elif data["_class"] == "lecture":
            chapters[index].add(data)
    return filter(is_int,chapters)

def get_course_url(url):
    pass
def get_courses_ids():
    li = []
    url= COURSE_IDS_GET_URL.replace("page_index","1").replace("pages","20")
    resp=session.get(url,params={"page":"1","page_size":"20"},verify=False)
    jsons = resp.json()
    if int(jsons["count"])<20:
        for course in jsons["results"]:
                li.append({"id":course['id'],"title":course["title"]})
    else:
        resp=session.get(url,params={"page":"1","page_size":jsons["count"]})
        for course in jsons["results"]:
            li.append({"id":course['id'],"title":course["title"]})
    return li
def get_video_message(course_id,id):
    url = URLMESDSSAGE.replace("video_id",str(id)).replace("course_id",str(course_id))
    respone=session.get(url,verify=False)
    jsondata=respone.json()
    try:
        return {"name":jsondata["title"],"url":jsondata["asset"]["stream_urls"]["Video"][0]["file"]}
    except:
        return {"name":"none"}
def down_load_mp4(url,path_filename):
    try:
        with open(BASEPATH+"downloadsuccesslog.txt","r+",encoding="utf-8") as f:
            strs = f.read()
        if len(re.findall(path_filename,strs))!=0:
            print("it is existed")
            return
    except:
        f = open(BASEPATH+"downloadsuccesslog.txt","w+",encoding="utf-8")
        f.close()
    try:
        print("It is ready to start %s"%(url))
        resp=session.get(url,verify=False)
    except Exception as ce:
        print(ce)
    if len(resp.content)>100000:
        with open(path_filename,"wb+") as f:
            f.write(resp.content)
        with open(BASEPATH+"downloadsuccesslog.txt","a+",encoding="utf-8") as f:
            f.write("%s\n"%(path_filename))
            print("download succeed ",path_filename)
    else:
        down_load_again(path_filename,url)
def down_load_again(path,url):
    global downloadlist
    downloadlist.put({"path":path,"url":url})

def creat_dir(name):

    try:
        os.mkdir(name)
    except Exception as ce:
        print(ce)
        pass

def checkdownload():
    while not downloadlist.empty():
        item = downloadlist.get()
        print(item)
        try:
            resp=session.get(item["url"])
            if len(resp.content)>100000:
                with open(item["path"],"wb+") as f:
                    f.write(resp.content)
            else:
                downloadlist.put(item)
        except Exception as ce:
            if item not in downloadlist:
                downloadlist.put(item)

def get_creat_path(*paths,filename=None):
    finally_path=BASEPATH
    for path in paths:
        finally_path+="".join(list(filter(is_alpha,path.replace(" ","_"))))+"/"

    if filename != None:
        filename = "".join(list(filter(is_alpha,filename.replace(" ","_"))))
        finally_path =finally_path+filename+".mp4"

    return  finally_path
def is_alpha(data):
    if data == "_" or data== "-":
        return True
    return data.isalnum()

if __name__ == '__main__':
    for course in get_courses_ids(): # 获得全部的course 的id与name
        print("program is start")
        creat_dir(get_creat_path(course["title"]))
        chapters=get_tree(course["id"])
        for chapter in chapters:
            qc.put(chapter)
        threads=[]
        for i in range(THREAD_NUM):
            thread = Mythread(qc,course["title"],course["id"])
            thread.start()
            threads.append(thread)

        for j in threads:
            j.join()
        checkdownload()

