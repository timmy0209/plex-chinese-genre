## python 3
# pip install plexapi
# 更多中文插件 请访问plexmedia.cn

import urllib
import http.client
import json
import sys
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
from plexapi.myplex import MyPlexDevice

PLEX_TOKEN = ""
tags = {
        "Action":"动作",
        "Adventure":"冒险",
        "Animation" :"动画",
        "Comedy":"喜剧",
        "Crime":"犯罪",
        "Documentary":"纪录",
        "Drama":"剧情",
        "Family":"家庭",
        "Fantasy":"奇幻",
        "History":"历史",
        "Horror":"恐怖",
        "Music":"音乐",
        "Mystery":"悬疑",
        "Romance":"爱情",
        "Science Fiction":"科幻",
        "Sport":"体育",
        "Thriller":"惊悚",
        "War":"战争",
        "Western":"西部",
        "Biography":"传记",
        "Film-noir":"黑色",
        "Musical":"音乐",
        "Sci-Fi":"科幻",
        "Tv Movie":"电视",
        "Disaster":"灾难",
        }
def fetchPlexApi(path='', method='GET', getFormPlextv=False, token=PLEX_TOKEN, params=None):
        """a helper function that fetches data from and put data to the plex server"""
        headers = {'X-Plex-Token': token,
                'Accept': 'application/json'}
        if getFormPlextv:
            url = 'plex.tv'        
            connection = http.client.HTTPSConnection(url)
        else:
            url = PLEX_URL.rstrip('/').replace('http://','')     
            connection = http.client.HTTPConnection(url)
        try:
            if method.upper() == 'GET':
                pass
            elif method.upper() == 'POST':
                headers.update({'Content-type': 'application/x-www-form-urlencoded'})
                pass
            elif method.upper() == 'PUT':
                pass
            elif method.upper() == 'DELETE':
                pass
            else:
                print("Invalid request method provided: {method}".format(method=method))
                connection.close()
                return

            connection.request(method.upper(), path , params, headers)     
            response = connection.getresponse()         
            r = response.read()             
            contentType = response.getheader('Content-Type')      
            status = response.status    
            connection.close()

            if response and len(r):     
                if 'application/json' in contentType:         
                    return json.loads(r)
                elif 'application/xml' in contentType:
                    return xmltodict.parse(r)
                else:
                    return r
            else:
                return r

        except Exception as e:
            connection.close()
            print("Error fetching from Plex API: {err}".format(err=e))

def updategenre(rating,genre):
        for tag in genre:
                try:
                        enggenre = tag["tag"]
                        enggenre =urllib.parse.quote(enggenre.encode('utf-8'))
                        zhQuery = tags[tag["tag"]]
                        zhQuery =urllib.parse.quote(zhQuery.encode('utf-8'))                               
                        data = fetchPlexApi("/library/sections/"+sectionNum+"/all?type=1&id="+rating+"&genre%5B2%5D.tag.tag="+zhQuery+"&genre%5B%5D.tag.tag-="+enggenre+"&", "PUT",token=PLEX_TOKEN)
                except:
                        pass
                

def getgenre(rating):
    url = "/library/metadata/"+rating+"?checkFiles=1"
    metadata = fetchPlexApi(url,token=PLEX_TOKEN)
    container = metadata["MediaContainer"]
    elements = container["Metadata"]
    for movie in elements:
        genre = movie["Genre"]
        updategenre(rating,genre)


def loopThroughAllMovies():
    toDo = True
    start = 0
    size = 5
    while toDo:
        if len(sectionNum):
            url = "/library/sections/" + sectionNum + "/all?type=1&X-Plex-Container-Start=%i&X-Plex-Container-Size=%i" % (start, size)
            metadata = fetchPlexApi(url,token=PLEX_TOKEN)
            container = metadata["MediaContainer"]
            elements = container["Metadata"]
            totalSize = container["totalSize"]
            offset = container["offset"]
            size = container["size"]      
            start = start + size        
            if totalSize-offset-size == 0:
                toDo = False
            for movie in elements:
                mediaType = movie["type"]
                if mediaType != "movie":
                     continue
                if "Genre" not in movie:
                     continue   
                key = movie["ratingKey"]        
                title = movie["title"]
                print(title)
                getgenre(key)

                
if __name__ == '__main__':

    #got token.url
    print("欢迎使用PLEX中文电影类型")
    PLEX_URL = input('请输入你的plex服务器地址：')
    PLEX_TOKEN = input('请输入你的token：')
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    for section in plex.library.sections():
            if section.type == 'movie':
               print(section)

    #choose list
    sectionNum = input('请输入你要排序的电影库编号：')
    
    # run at startup
    loopThroughAllMovies()
    

