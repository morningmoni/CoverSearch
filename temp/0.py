#encoding=utf8
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
import urlparse
import time
import socket
import os
import urllib
import re
from datetime import datetime


def clip(a):
    ty=''
    net='http://www.xiami.com/'
    if len(a)<18:
        return None,None
    #print 1
    if a[:21]!='http://www.xiami.com/':
        return None,None
    a=a[21:]
    #print 2
    try:
        if a[:5]=='song/':
            #ty='song'
            a=a[5:]
            net=net+'song/'
        elif a[:6]=='album/':
            #ty='album'
            a=a[6:]
            net=net+'album/'
        elif a[:7]=='artist/':
            #ty='artist'
            a=a[7:]
            net=net+'artist/'
    except:
        return None,None
    for i in range(len(a)):
        if a[i] in ['0','1','2','3','4','5','6','7','8','9']:
            net=net+a[i]
        else:
            break
    return net


def get_albums(url):
    global s
    a=url.split('/')
    a=a[-1]
    a='http://www.xiami.com/artist/album-'+a+'?page='
    i=0
    result=[]
    names=[]
    while(1):
        i+=1 
        b=a+str(i)
        #time.sleep(10.0)
        req = urllib2.Request(b)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        try:
            content=urllib2.urlopen(req,timeout=5).read()
        except:
            return result,names
        soup=BeautifulSoup(content)
        lis=soup.find('ul',{'class':'clearfix'}).findAll('li')
        for li in lis:
            
            tmp=li.find('p',{'class':'name'})
            if(tmp==None):
                continue
            result.append(s+str(tmp.a.get('href')))
            names.append(tmp.a.text.encode('utf-8'))
           
        for j in range(len(result)):
            result[j]=clip(result[j])
        if '下一页' not in content:
            break
        else:
            print i
            pass
        
    return result,names



def get_songs(url,content):
    global s
    result=[]
    names=[]
    soup=BeautifulSoup(content)
    a=soup.findAll('td',{'class':'song_name'})
    for item in a:
        result.append(s+str(item.a.get('href')))
        names.append(item.a.text.encode('utf-8'))
    return result,names
    
def creat_artist(url,albums,albumURLs):
    #time.sleep(10.0)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    try:
        content=urllib2.urlopen(req,timeout=5).read()
    except:
        return False
    soup=BeautifulSoup(content)
    a=url.split('/')
    a=a[-1]
    fil=open('texts/artist/'+a+'.txt','w')
    fil.write('number ')
    fil.write(a)
    fil.write('\n')
    a=soup.body.find(id='page')
    print '\n'
    try:
        fil.write('name ')
        fil.write(a.find(id='wrapper').find(id='title').h1.text.encode('utf-8'))
        fil.write('\n')
    except:
        pass
    try:
        fil.write('place ')
        fil.write(a.find(id="artist_info").findAll(valign="top")[1].text.encode('utf-8'))
        fil.write('\n')
    except:
        pass
    try:
        fil.write('introduction ')
        fil.write(a.find("table").find("div").text.encode('utf-8'))
        fil.write('\n')
    except:
        pass
    try:
        fil.write('picture ')
        fil.write(a.find(id="cover_lightbox")["href"].encode('utf-8'))
        fil.write('\n')
    except:
        pass
    try:
        fil.write('albums ')
        for item in albums:
            fil.write(item)
            fil.write('%^&*')
        fil.write('\n')
        fil.write('albumURLs ')
        for item in albumURLs:
            fil.write(item)
            fil.write('%^&*')
    except:
        pass
        

    fil.close()
    return True
    
    
def creat_album(url,content,songs,songURLs):
    soup=BeautifulSoup(content)
    a=url.split('/')
    a=a[-1]
    fil=open('texts/album/'+a+'.txt','w')
    of=open('texts/picture/'+a+'.jpg','wb')
    
    
    fil.write('number ')
    fil.write(a)
    fil.write('\n')
    a=soup.body.find(id='page').find(id='main').find(id='album_cover')
    
    
    
    a=a.find('a')
    try:
        fil.write('name ')
        fil.write(a.get('title').encode('utf-8'))
        fil.write('\n')
    except:
        pass
    try:
        fil.write('artist ')
        fil.write(soup.find(id='album_block').findAll(valign='top')[1].text.encode('utf-8'))
        fil.write('\n')
    except:
        pass
    try:
        fil.write('introduction ')
        fil.write(soup.find('span',{'property':'v:summary'}).text.encode('utf-8'))
        fil.write('\n')
    except:
        pass
    try:
        fil.write('picture ')
        fil.write(a.get('href'))
    except:
        pass
    
    try:     
        req = urllib2.Request(a.get('href'))
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        q=urllib2.urlopen(req,timeout=5).read()
        of.write(q)
        of.close()
    except:
        of.close()
        
    fil.write('\n')
    fil.write('songs ')
    for item in songs:
        fil.write(item)
        fil.write('%^&*')
    fil.write('\n')
    fil.write('songURLs ')
    for item in songURLs:
        fil.write(item)
        fil.write('%^&*')
    
    fil.close()
    return True



def creat_song(url):
    global s
    #time.sleep(10.0)
    req = urllib2.Request(url)

    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    try:
        content=urllib2.urlopen(req,timeout=5).read()
    except:
        return False
    soup=BeautifulSoup(content)
    a=url.split('/')
    a=a[-1]
    fil=open('texts/song/'+a+'.txt','w')
    fil.write('number ')
    fil.write(a)
    fil.write('\n')
    try:
        fil.write('name ')
        fil.write(soup.find(id='page').find(id='title').text.encode('utf-8'))
        fil.write('\n')
    except:
        pass
    try:
        fil.write('artist ')
        tmp=soup.find('div',id='song_block').find('table',id='albums_info').findAll('td',{'valign':'top'})[3].div.findAll('a')
        for item in tmp:
            fil.write(item.text.encode('utf-8'))
            fil.write('%^&*')
        fil.write('\n')
        fil.write('artistURL ')
        for item in tmp:
            fil.write(s+str(item.get('href')))
            fil.write('%^&*')
            fil.write('\n')
    except:
        pass
    try:
        fil.write('album ')
        fil.write(soup.find('div',id='song_block').find('table',id='albums_info').findAll('td',{'valign':'top'})[1].div.a.text.encode('utf-8'))
        fil.write('\n')
        fil.write('albumURL ')
        fil.write(s+str(soup.find('div',id='song_block').find('table',id='albums_info').findAll('td',{'valign':'top'})[1].div.a.get('href')))
    except:
        pass
    fil.close()
    return True
    
    
    
            
count=0
i=0
s='http://www.xiami.com'        
    
    


    


count=0
i=raw_input('从第几号歌手开始爬?')
i=int(i)

s='http://www.xiami.com'
while(1):
    
    
    url=s+'/artist/'+str(i)
    
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    try:
        content=urllib2.urlopen(req,timeout=5).read()
        count=0
    except Exception,e:
        print e
        count+=1
        continue
    time.sleep(5)
    if count>=25 and i>100000:
        break

    
    
    albums,albumnames=get_albums(url)
    if(len(albums)==0):
        continue
  
    creat_artist(url,albumnames,albums)
    print 'finish',i,'artist'
    for album in albums:
        #time.sleep(10.0)
        req = urllib2.Request(album)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        try:
            content=urllib2.urlopen(req,timeout=5).read()
        except:
            continue
        songs,songnames=get_songs(album,content)
        creat_album(album,content,songnames,songs)
        print 'finish',i,'album'
        
        for song in songs:
            creat_song(song)
            print 'finish',i,'song'
    i+=1
            


